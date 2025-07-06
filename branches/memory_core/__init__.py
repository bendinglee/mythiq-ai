# 🧠 SELF-LEARNING AI BRAIN INITIALIZER
# This starts up the learning system

from .controller import memory_api

# Brain information
BRANCH_NAME = "Memory Core"
BRANCH_VERSION = "2.0.0"
BRANCH_DESCRIPTION = "Self-learning AI memory and feedback system"

# Learning capabilities
CAPABILITIES = [
    "conversation_memory",
    "feedback_learning", 
    "pattern_recognition",
    "similarity_search",
    "confidence_scoring",
    "learning_analytics"
]

# API endpoints
ENDPOINTS = [
    {"path": "/memory/learn", "method": "POST", "description": "Learn from user interactions"},
    {"path": "/memory/recall", "method": "POST", "description": "Recall similar conversations"},
    {"path": "/memory/feedback", "method": "POST", "description": "Update feedback on responses"},
    {"path": "/memory/stats", "method": "GET", "description": "Get learning statistics"}
]

def get_branch_info():
    """Get information about this learning branch"""
    return {
        "name": BRANCH_NAME,
        "version": BRANCH_VERSION,
        "description": BRANCH_DESCRIPTION,
        "capabilities": CAPABILITIES,
        "endpoints": ENDPOINTS,
        "status": "active",
        "learning_enabled": True
    }

def initialize_branch():
    """Initialize the self-learning memory branch"""
    print(f"🧠 Initializing {BRANCH_NAME} v{BRANCH_VERSION}")
    print(f"📚 Learning capabilities: {len(CAPABILITIES)}")
    print(f"🔗 API endpoints: {len(ENDPOINTS)}")
    print("🎓 Self-learning system ready!")
    return True

# Export everything
__all__ = ['memory_api', 'get_branch_info', 'initialize_branch']
