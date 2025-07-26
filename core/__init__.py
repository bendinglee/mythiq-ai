Mythiq AI - Core Intelligence Modules
Stage 2: Real AI Intelligence with Emotional Understanding

This package contains the core intelligence systems that power Mythiq's
advanced AI capabilities including memory management, diagnostics, and
resilience systems.
"""

__version__ = "2.0.0"
__stage__ = "Stage 2 - AI Intelligence"

# Core module exports
from .memory import MemoryManager
from .diagnostics import DiagnosticsManager  
from .fallback import FallbackManager

__all__ = [
    'MemoryManager',
    'DiagnosticsManager', 
    'FallbackManager'
]
