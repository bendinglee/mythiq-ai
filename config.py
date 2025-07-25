"""
Mythiq Configuration
Central configuration management for the Mythiq AI platform
"""

import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mythiq-dev-key-2025-secure')
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Server Configuration
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # Data Directories
    DATA_DIR = os.environ.get('DATA_DIR', 'data')
    LOGS_DIR = os.path.join(DATA_DIR, 'logs')
    FEEDBACK_DIR = os.path.join(DATA_DIR, 'feedback')
    MEMORY_FILE = os.path.join(DATA_DIR, 'memory_store.json')
    
    # AI Service Configuration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
    OPENAI_API_BASE = os.environ.get('OPENAI_API_BASE', 'https://api.openai.com/v1')
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
    
    # Performance Thresholds
    RESPONSE_TIME_THRESHOLD = float(os.environ.get('RESPONSE_TIME_THRESHOLD', 5.0))
    MEMORY_USAGE_THRESHOLD = float(os.environ.get('MEMORY_USAGE_THRESHOLD', 80.0))
    CPU_USAGE_THRESHOLD = float(os.environ.get('CPU_USAGE_THRESHOLD', 80.0))
    ERROR_RATE_THRESHOLD = float(os.environ.get('ERROR_RATE_THRESHOLD', 5.0))
    
    # Circuit Breaker Configuration
    CIRCUIT_BREAKER_FAILURE_THRESHOLD = int(os.environ.get('CIRCUIT_BREAKER_FAILURE_THRESHOLD', 5))
    CIRCUIT_BREAKER_TIMEOUT = int(os.environ.get('CIRCUIT_BREAKER_TIMEOUT', 60))
    
    # Retry Configuration
    MAX_RETRIES = int(os.environ.get('MAX_RETRIES', 3))
    BACKOFF_FACTOR = float(os.environ.get('BACKOFF_FACTOR', 2.0))
    MAX_RETRY_DELAY = float(os.environ.get('MAX_RETRY_DELAY', 60.0))
    
    # Memory Management
    MAX_CONVERSATIONS_PER_USER = int(os.environ.get('MAX_CONVERSATIONS_PER_USER', 100))
    MAX_LEARNING_ENTRIES_PER_CATEGORY = int(os.environ.get('MAX_LEARNING_ENTRIES_PER_CATEGORY', 1000))
    VOLATILE_MEMORY_TTL = int(os.environ.get('VOLATILE_MEMORY_TTL', 3600))  # 1 hour
    
    # Monitoring Configuration
    METRICS_COLLECTION_INTERVAL = int(os.environ.get('METRICS_COLLECTION_INTERVAL', 30))  # seconds
    HEALTH_CHECK_INTERVAL = int(os.environ.get('HEALTH_CHECK_INTERVAL', 60))  # seconds
    DATA_RETENTION_DAYS = int(os.environ.get('DATA_RETENTION_DAYS', 7))
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE = int(os.environ.get('RATE_LIMIT_PER_MINUTE', 60))
    RATE_LIMIT_PER_HOUR = int(os.environ.get('RATE_LIMIT_PER_HOUR', 1000))
    
    # Generation Limits
    MAX_GAME_GENERATIONS_PER_HOUR = int(os.environ.get('MAX_GAME_GENERATIONS_PER_HOUR', 10))
    MAX_IMAGE_GENERATIONS_PER_HOUR = int(os.environ.get('MAX_IMAGE_GENERATIONS_PER_HOUR', 20))
    MAX_VIDEO_GENERATIONS_PER_HOUR = int(os.environ.get('MAX_VIDEO_GENERATIONS_PER_HOUR', 5))
    
    # Security Configuration
    ENABLE_CORS = os.environ.get('ENABLE_CORS', 'True').lower() == 'true'
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_MAX_BYTES = int(os.environ.get('LOG_MAX_BYTES', 10485760))  # 10MB
    LOG_BACKUP_COUNT = int(os.environ.get('LOG_BACKUP_COUNT', 5))

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    
    # Stricter thresholds for production
    RESPONSE_TIME_THRESHOLD = 3.0
    MEMORY_USAGE_THRESHOLD = 70.0
    CPU_USAGE_THRESHOLD = 70.0
    ERROR_RATE_THRESHOLD = 2.0
    
    # More conservative rate limits
    RATE_LIMIT_PER_MINUTE = 30
    RATE_LIMIT_PER_HOUR = 500
    
    MAX_GAME_GENERATIONS_PER_HOUR = 5
    MAX_IMAGE_GENERATIONS_PER_HOUR = 10
    MAX_VIDEO_GENERATIONS_PER_HOUR = 2

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    
    # Use in-memory storage for testing
    DATA_DIR = '/tmp/mythiq_test'
    
    # Relaxed thresholds for testing
    RESPONSE_TIME_THRESHOLD = 10.0
    CIRCUIT_BREAKER_FAILURE_THRESHOLD = 10

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(config_name=None):
    """Get configuration class based on environment"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    return config.get(config_name, DevelopmentConfig)

