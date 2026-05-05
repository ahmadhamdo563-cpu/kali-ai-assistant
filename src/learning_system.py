"""Learning and Parameter Optimization Module"""

import json
import os
import sqlite3
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging
import numpy as np
from collections import defaultdict, Counter

logger = logging.getLogger(__name__)

class LearningSystem:
    """Advanced learning system that optimizes parameters based on usage patterns"""
    
    def __init__(self, db_path: str = "./kali_learning.db"):
        """Initialize learning system with encrypted storage"""
        self.db_path = db_path
        self.learning_enabled = True
        self.parameters = self._load_default_parameters()
        self._init_database()
        self._load_learned_parameters()
    
    def _load_default_parameters(self) -> Dict[str, float]:
        """Load default Groq parameters"""
        return {
            "temperature": 0.7,
            "top_p": 1.0,
            "presence_penalty": 0.0,
            "frequency_penalty": 0.0,
            "response_length": 2048,
            "creativity_level": 0.5,
        }
    
    def _init_database(self):
        """Initialize SQLite database for learning"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Interactions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query_hash TEXT NOT NULL,
                    query TEXT NOT NULL,
                    response TEXT NOT NULL,
                    timestamp REAL NOT NULL,
                    query_type TEXT,
                    response_quality REAL,
                    user_satisfaction INTEGER,
                    parameters_used TEXT,
                    tokens_used INTEGER,
                    response_time REAL
                )
            """)
            
            # Learning metrics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS learning_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_name TEXT UNIQUE,
                    metric_value REAL,
                    last_updated REAL
                )
            """)
            
            # Query patterns table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS query_patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pattern TEXT UNIQUE,
                    frequency INTEGER DEFAULT 1,
                    avg_quality REAL,
                    optimal_parameters TEXT
                )
            """)
            
            # User communication style table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS communication_style (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    style_attribute TEXT UNIQUE,
                    value REAL,
                    samples INTEGER
                )
            """)
            
            conn.commit()
            conn.close()
            logger.info("Learning database initialized")
        except Exception as e:
            logger.error(f"Error initializing learning database: {str(e)}")
    
    def analyze_interaction(self, query: str, response: str, 
                          quality_score: float, satisfaction: int = 0,
                          parameters: Dict = None, tokens: int = 0,
                          response_time: float = 0.0) -> bool:
        """Analyze and learn from each interaction"""
        try:
            query_hash = hashlib.sha256(query.lower().encode()).hexdigest()
            query_type = self._classify_query(query)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Store interaction
            cursor.execute("""
                INSERT INTO interactions 
                (query_hash, query, response, timestamp, query_type, response_quality, 
                 user_satisfaction, parameters_used, tokens_used, response_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                query_hash, query, response, datetime.now().timestamp(),
                query_type, quality_score, satisfaction,
                json.dumps(parameters or {}), tokens, response_time
            ))
            
            # Extract patterns from successful responses
            if quality_score > 0.7:
                self._extract_and_store_pattern(cursor, query, query_type, parameters)
            
            # Analyze communication style
            self._analyze_style(cursor, query, response)
            
            # Update metrics
            self._update_metrics(cursor, query_type, quality_score)
            
            conn.commit()
            conn.close()
            
            # Re-optimize parameters if enough data
            if self._has_sufficient_data():
                self._optimize_parameters()
            
            return True
        except Exception as e:
            logger.error(f"Error analyzing interaction: {str(e)}")
            return False
    
    def _classify_query(self, query: str) -> str:
        """Classify query type for optimization"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['exploit', 'vulnerability', 'attack', 'penetration']):
            return 'security'
        elif any(word in query_lower for word in ['code', 'function', 'algorithm', 'debug']):
            return 'coding'
        elif any(word in query_lower for word in ['network', 'packet', 'port', 'firewall']):
            return 'networking'
        elif any(word in query_lower for word in ['linux', 'bash', 'shell', 'system']):
            return 'system_admin'
        else:
            return 'general'
    
    def _extract_and_store_pattern(self, cursor, query: str, query_type: str, 
                                   parameters: Dict = None):
        """Extract successful patterns from high-quality responses"""
        # Extract keywords
        words = set(query.lower().split())
        pattern_key = f"{query_type}_{len(query)}"  # Pattern signature
        
        cursor.execute("""
            INSERT OR REPLACE INTO query_patterns 
            (pattern, frequency, optimal_parameters)
            VALUES (?, 
                    (SELECT frequency FROM query_patterns WHERE pattern = ?) + 1,
                    ?)
        """, (pattern_key, pattern_key, json.dumps(parameters or {})))
    
    def _analyze_style(self, cursor, query: str, response: str):
        """Analyze user communication style"""
        # Analyze query length preference
        query_len = len(query.split())
        response_len = len(response.split())
        
        # Analyze formality (simplified)
        formal_indicators = ['please', 'kindly', 'would', 'could', 'appreciate']
        formality_score = sum(1 for indicator in formal_indicators if indicator in query.lower()) / len(formal_indicators)
        
        cursor.execute("""
            INSERT OR REPLACE INTO communication_style 
            (style_attribute, value, samples)
            VALUES (?, ?, 
                    (SELECT samples FROM communication_style WHERE style_attribute = ?) + 1)
        """, ('preferred_response_length', response_len, 'preferred_response_length'))
        
        cursor.execute("""
            INSERT OR REPLACE INTO communication_style 
            (style_attribute, value, samples)
            VALUES (?, ?, 
                    (SELECT samples FROM communication_style WHERE style_attribute = ?) + 1)
        """, ('formality_preference', formality_score, 'formality_preference'))
    
    def _update_metrics(self, cursor, query_type: str, quality_score: float):
        """Update learning metrics"""
        metric_key = f"{query_type}_quality"
        cursor.execute("""
            INSERT OR REPLACE INTO learning_metrics 
            (metric_name, metric_value, last_updated)
            VALUES (?, ?, ?)
        """, (metric_key, quality_score, datetime.now().timestamp()))
    
    def _has_sufficient_data(self) -> bool:
        """Check if enough data for optimization"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM interactions")
            count = cursor.fetchone()[0]
            conn.close()
            return count >= 20  # Threshold for optimization
        except:
            return False
    
    def _optimize_parameters(self) -> Dict[str, float]:
        """Optimize parameters based on learned patterns"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get average quality scores by query type
            cursor.execute("""
                SELECT query_type, AVG(response_quality) as avg_quality
                FROM interactions
                WHERE timestamp > datetime('now', '-7 days')
                GROUP BY query_type
            """)
            
            quality_by_type = {row[0]: row[1] for row in cursor.fetchall()}
            
            # Adjust temperature based on quality
            # Higher quality = maintain current temp, lower quality = increase creativity
            avg_quality = np.mean(list(quality_by_type.values())) if quality_by_type else 0.5
            
            if avg_quality < 0.6:
                self.parameters['temperature'] = min(0.9, self.parameters['temperature'] + 0.05)
                self.parameters['top_p'] = min(1.0, self.parameters['top_p'] + 0.05)
            elif avg_quality > 0.85:
                self.parameters['temperature'] = max(0.5, self.parameters['temperature'] - 0.05)
            
            # Get user satisfaction patterns
            cursor.execute("""
                SELECT AVG(user_satisfaction) FROM interactions 
                WHERE user_satisfaction > 0
            """)
            avg_satisfaction = cursor.fetchone()[0] or 0
            
            if avg_satisfaction > 0:
                self.parameters['response_length'] = int(2048 + (avg_satisfaction * 100))
            
            conn.close()
            
            # Save optimized parameters
            self._save_learned_parameters()
            logger.info(f"Parameters optimized: {self.parameters}")
            
            return self.parameters
            
        except Exception as e:
            logger.error(f"Error optimizing parameters: {str(e)}")
            return self.parameters
    
    def get_optimized_parameters(self, query_type: str = 'general') -> Dict[str, Any]:
        """Get optimized parameters for specific query type"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get best parameters for this query type
            cursor.execute("""
                SELECT AVG(response_quality), optimal_parameters
                FROM query_patterns
                WHERE pattern LIKE ?
                ORDER BY frequency DESC
                LIMIT 1
            """, (f"{query_type}%",))
            
            result = cursor.fetchone()
            conn.close()
            
            if result and result[1]:
                return json.loads(result[1])
            
            return self.parameters
        except Exception as e:
            logger.error(f"Error getting optimized parameters: {str(e)}")
            return self.parameters
    
    def _save_learned_parameters(self):
        """Save learned parameters to file (encrypted in production)"""
        try:
            with open('.learned_params.json', 'w') as f:
                json.dump({
                    'parameters': self.parameters,
                    'timestamp': datetime.now().isoformat(),
                    'version': '1.0'
                }, f, indent=4)
            logger.info("Learned parameters saved")
        except Exception as e:
            logger.error(f"Error saving parameters: {str(e)}")
    
    def _load_learned_parameters(self):
        """Load previously learned parameters"""
        try:
            if os.path.exists('.learned_params.json'):
                with open('.learned_params.json', 'r') as f:
                    data = json.load(f)
                    self.parameters.update(data.get('parameters', {}))
                    logger.info("Learned parameters loaded")
        except Exception as e:
            logger.error(f"Error loading parameters: {str(e)}")
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """Get comprehensive learning statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM interactions")
            total_interactions = cursor.fetchone()[0]
            
            cursor.execute("SELECT AVG(response_quality) FROM interactions")
            avg_quality = cursor.fetchone()[0] or 0
            
            cursor.execute("""
                SELECT query_type, COUNT(*), AVG(response_quality)
                FROM interactions
                GROUP BY query_type
            """)
            
            query_type_stats = cursor.fetchall()
            
            cursor.execute("SELECT COUNT(DISTINCT query_hash) FROM interactions")
            unique_queries = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'total_interactions': total_interactions,
                'unique_queries': unique_queries,
                'average_quality': round(avg_quality, 3),
                'current_parameters': self.parameters,
                'query_type_breakdown': [
                    {'type': row[0], 'count': row[1], 'avg_quality': round(row[2], 3)}
                    for row in query_type_stats
                ]
            }
        except Exception as e:
            logger.error(f"Error getting learning stats: {str(e)}")
            return {}
