"""
Mythiq AI - Intelligence Modules
Stage 2: Advanced AI Intelligence and Emotional Understanding

This package contains the AI intelligence modules that power Mythiq's
advanced reasoning, emotional intelligence, and conversation capabilities.
"""

__version__ = "2.0.0"
__stage__ = "Stage 2 - AI Intelligence"

# Intelligence module exports
from .reasoning_engine import ReasoningEngine
from .chat_core import ChatCore
from .ai_services import AIServiceManager
from .reflector import ReflectorModule

__all__ = [
    'ReasoningEngine',
    'ChatCore', 
    'AIServiceManager',
    'ReflectorModule'
]
