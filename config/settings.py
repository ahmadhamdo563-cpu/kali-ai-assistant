"""Configuration settings for Kali AI Assistant"""

import os
from typing import Optional

class Settings:
    """Application settings"""
    
    # API Configuration
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    MODEL: str = os.getenv("MODEL", "mixtral-8x7b-32768")
    
    # Voice Configuration
    VOICE_ENABLED: bool = os.getenv("VOICE_ENABLED", "true").lower() == "true"
    VOICE_LANGUAGE: str = os.getenv("VOICE_LANGUAGE", "en-US")
    VOICE_RATE: int = int(os.getenv("VOICE_RATE", "150"))
    
    # Cache Configuration
    CACHE_ENABLED: bool = os.getenv("CACHE_ENABLED", "true").lower() == "true"
    CACHE_EXPIRY: int = int(os.getenv("CACHE_EXPIRY", "86400"))  # 24 hours
    CACHE_DB_PATH: str = os.getenv("CACHE_DB_PATH", "./kali_cache.db")
    
    # Assistant Configuration
    ASSISTANT_NAME: str = os.getenv("ASSISTANT_NAME", "Kali")
    DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "false").lower() == "true"
    
    # Logging Configuration
    LOG_FILE: str = "kali_assistant.log"
    LOG_LEVEL: str = "DEBUG" if DEBUG_MODE else "INFO"
    
    # Response Configuration
    MAX_TOKENS: int = 2048
    TEMPERATURE: float = 0.7
    TOP_P: float = 1.0
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration"""
        if not cls.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not set")
        return True
