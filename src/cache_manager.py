"""Cache Management Module for query caching"""

import sqlite3
import hashlib
import json
import os
import time
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class CacheManager:
    """Manages query caching using SQLite"""
    
    def __init__(self, db_path: str = "./kali_cache.db"):
        """Initialize cache manager"""
        self.db_path = db_path
        self.enabled = os.getenv("CACHE_ENABLED", "true").lower() == "true"
        self.expiry_seconds = int(os.getenv("CACHE_EXPIRY", "86400"))  # 24 hours default
        
        if self.enabled:
            self._init_database()
    
    def _init_database(self):
        """Initialize SQLite database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cache (
                    query_hash TEXT PRIMARY KEY,
                    query TEXT NOT NULL,
                    response TEXT NOT NULL,
                    timestamp REAL NOT NULL,
                    hits INTEGER DEFAULT 0
                )
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp 
                ON cache(timestamp)
            """)
            
            conn.commit()
            conn.close()
            logger.info("Cache database initialized")
        except Exception as e:
            logger.error(f"Error initializing cache database: {str(e)}")
            self.enabled = False
    
    def _hash_query(self, query: str) -> str:
        """Generate hash of query"""
        return hashlib.sha256(query.lower().encode()).hexdigest()
    
    def get(self, query: str) -> Optional[str]:
        """Get cached response for query"""
        if not self.enabled:
            return None
        
        try:
            query_hash = self._hash_query(query)
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT response, timestamp, hits FROM cache WHERE query_hash = ?",
                (query_hash,)
            )
            
            result = cursor.fetchone()
            
            if result:
                response, timestamp, hits = result
                current_time = time.time()
                
                # Check if cache is expired
                if current_time - timestamp > self.expiry_seconds:
                    cursor.execute("DELETE FROM cache WHERE query_hash = ?", (query_hash,))
                    conn.commit()
                    conn.close()
                    return None
                
                # Update hit count
                cursor.execute(
                    "UPDATE cache SET hits = hits + 1 WHERE query_hash = ?",
                    (query_hash,)
                )
                conn.commit()
                conn.close()
                
                logger.info(f"Cache hit for: {query[:50]}...")
                return response
            
            conn.close()
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving from cache: {str(e)}")
            return None
    
    def set(self, query: str, response: str) -> bool:
        """Cache a query and response"""
        if not self.enabled:
            return False
        
        try:
            query_hash = self._hash_query(query)
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                """
                INSERT OR REPLACE INTO cache (query_hash, query, response, timestamp, hits)
                VALUES (?, ?, ?, ?, 0)
                """,
                (query_hash, query, response, time.time())
            )
            
            conn.commit()
            conn.close()
            
            logger.info(f"Cached: {query[:50]}...")
            return True
            
        except Exception as e:
            logger.error(f"Error caching query: {str(e)}")
            return False
    
    def clear(self) -> bool:
        """Clear all cache"""
        if not self.enabled:
            return False
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM cache")
            conn.commit()
            conn.close()
            logger.info("Cache cleared")
            return True
        except Exception as e:
            logger.error(f"Error clearing cache: {str(e)}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        if not self.enabled:
            return {}
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM cache")
            total_cached = cursor.fetchone()[0]
            
            cursor.execute("SELECT SUM(hits) FROM cache")
            total_hits = cursor.fetchone()[0] or 0
            
            cursor.execute("SELECT AVG(hits) FROM cache")
            avg_hits = cursor.fetchone()[0] or 0
            
            conn.close()
            
            return {
                "total_cached_queries": total_cached,
                "total_cache_hits": total_hits,
                "average_hits_per_query": round(avg_hits, 2)
            }
        except Exception as e:
            logger.error(f"Error getting cache stats: {str(e)}")
            return {}
