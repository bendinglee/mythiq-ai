"""
Mythiq AI - Stage 2 Configuration
Configuration settings for the emotional intelligence platform
"""

import os
from typing import Dict, Any

class Config:
    """Base configuration class."""
    
    # Application settings
    APP_NAME = "Mythiq AI - Stage 2"
    VERSION = "2.0.0"
    STAGE = "Stage 2 - AI Intelligence"
    
    # Server settings
    HOST = "0.0.0.0"
    PORT = int(os.environ.get('PORT', 8080))
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # AI Service API Keys
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
    
    # Memory settings
    MEMORY_CONFIG = {
        "max_conversations_per_user": 50,
        "max_learning_patterns": 1000,
        "memory_cleanup_interval": 3600,  # 1 hour
        "data_retention_days": 30
    }
    
    # Diagnostics settings
    DIAGNOSTICS_CONFIG = {
        "monitoring_interval": 30,  # seconds
        "alert_thresholds": {
            "response_time": 5.0,  # seconds
            "memory_usage": 80.0,  # percentage
            "cpu_usage": 80.0,     # percentage
            "error_rate": 10.0,    # percentage
            "disk_usage": 90.0     # percentage
        },
        "performance_history_size": 1000
    }
    
    # Reasoning engine settings
    REASONING_CONFIG = {
        "emotion_confidence_threshold": 0.6,
        "intent_confidence_threshold": 0.7,
        "context_analysis_depth": 5,  # messages to analyze
        "enable_advanced_patterns": True
    }
    
    # Chat core settings
    CHAT_CONFIG = {
        "max_conversation_history": 10,
        "default_response_style": "balanced",
        "default_personality": "balanced",
        "enable_suggestions": True,
        "suggestion_count": 3
    }
    
    # AI Services settings
    AI_SERVICES_CONFIG = {
        "default_timeout": 30.0,
        "max_retries": 3,
        "rate_limit_buffer": 0.8,  # Use 80% of rate limit
        "cost_tracking": True,
        "prefer_free_services": True
    }
    
    # Reflector settings
    REFLECTOR_CONFIG = {
        "min_interactions_for_pattern": 5,
        "confidence_threshold": 0.7,
        "reflection_interval": 3600,  # 1 hour
        "max_learning_patterns": 500,
        "enable_auto_improvement": True
    }
    
    # Fallback settings
    FALLBACK_CONFIG = {
        "global_timeout": 30.0,
        "max_fallback_levels": 5,
        "adaptive_routing": True,
        "circuit_breaker_threshold": 5,
        "circuit_breaker_timeout": 300  # 5 minutes
    }
    
    # Logging settings
    LOGGING_CONFIG = {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "file_logging": False,
        "log_file": "mythiq_stage2.log"
    }

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    LOGGING_CONFIG = {
        **Config.LOGGING_CONFIG,
        "level": "DEBUG"
    }

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    LOGGING_CONFIG = {
        **Config.LOGGING_CONFIG,
        "level": "WARNING",
        "file_logging": True
    }

class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    MEMORY_CONFIG = {
        **Config.MEMORY_CONFIG,
        "max_conversations_per_user": 10,
        "max_learning_patterns": 100
    }

# Configuration mapping
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(config_name: str = None) -> Config:
    """Get configuration based on environment."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    return config_map.get(config_name, DevelopmentConfig)

def get_ai_service_configs() -> Dict[str, Dict[str, Any]]:
    """Get AI service configurations."""
    configs = {}
    
    # OpenAI configuration
    if Config.OPENAI_API_KEY:
        configs['openai'] = {
            'name': 'openai',
            'api_key': Config.OPENAI_API_KEY,
            'base_url': 'https://api.openai.com/v1',
            'model': 'gpt-3.5-turbo',
            'max_tokens': 1000,
            'temperature': 0.7,
            'timeout': 30.0,
            'rate_limit_per_minute': 60,
            'cost_per_1k_tokens': 0.002,
            'priority': 2
        }
    
    # Anthropic Claude configuration
    if Config.ANTHROPIC_API_KEY:
        configs['claude'] = {
            'name': 'claude',
            'api_key': Config.ANTHROPIC_API_KEY,
            'base_url': 'https://api.anthropic.com/v1',
            'model': 'claude-3-haiku-20240307',
            'max_tokens': 1000,
            'temperature': 0.7,
            'timeout': 30.0,
            'rate_limit_per_minute': 50,
            'cost_per_1k_tokens': 0.00025,
            'priority': 1  # Highest priority for emotional intelligence
        }
    
    # Groq configuration
    if Config.GROQ_API_KEY:
        configs['groq'] = {
            'name': 'groq',
            'api_key': Config.GROQ_API_KEY,
            'base_url': 'https://api.groq.com/openai/v1',
            'model': 'llama3-8b-8192',
            'max_tokens': 1000,
            'temperature': 0.7,
            'timeout': 15.0,
            'rate_limit_per_minute': 100,
            'cost_per_1k_tokens': 0.0,  # Free tier
            'priority': 0  # Highest priority for speed
        }
    
    return configs

def validate_configuration() -> Dict[str, Any]:
    """Validate configuration and return status."""
    validation_results = {
        "valid": True,
        "warnings": [],
        "errors": [],
        "ai_services_configured": 0
    }
    
    # Check AI service configurations
    ai_configs = get_ai_service_configs()
    validation_results["ai_services_configured"] = len(ai_configs)
    
    if not ai_configs:
        validation_results["errors"].append("No AI services configured - check API keys")
        validation_results["valid"] = False
    elif len(ai_configs) == 1:
        validation_results["warnings"].append("Only one AI service configured - limited fallback options")
    
    # Check required environment variables
    required_env_vars = []
    optional_env_vars = ['OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'GROQ_API_KEY']
    
    for var in required_env_vars:
        if not os.environ.get(var):
            validation_results["errors"].append(f"Required environment variable {var} not set")
            validation_results["valid"] = False
    
    # Check if at least one AI service is configured
    if not any(os.environ.get(var) for var in optional_env_vars):
        validation_results["errors"].append("At least one AI service API key must be configured")
        validation_results["valid"] = False
    
    return validation_results

# Export main configuration
current_config = get_config()
