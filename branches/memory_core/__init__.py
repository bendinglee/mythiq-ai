# 🧠 SELF-LEARNING AI BRAIN INITIALIZER

from .routes import memory_api

# 📘 Branch Identity
BRANCH_NAME = "Memory Core"
BRANCH_VERSION = "2.0.0"
BRANCH_DESCRIPTION = "Self-learning AI memory and feedback system with pattern retention and long-term adaptation."

# 🧠 Learning Capabilities
CAPABILITIES = [
    "conversation_memory",
    "feedback_learning",
    "pattern_recognition",
    "similarity_search",
    "confidence_scoring",
    "learning_analytics"
]

# 🔗 API Endpoints
ENDPOINTS = [
    {"path": "/memory/log", "method": "POST", "description": "Log new memory entry"},
    {"path": "/memory/search", "method": "GET", "description": "Search memory entries"},
    {"path": "/memory/recall", "method": "POST", "description": "Recall similar conversations"},
    {"path": "/memory/feedback", "method": "POST", "description": "Update feedback on responses"},
    {"path": "/memory/stats", "method": "GET", "description": "Get learning statistics"}
]

def get_branch_info():
    """Expose metadata for introspection and UI display."""
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
    """Boot sequence logging for memory_core."""
    print(f"🧠 Booting {BRANCH_NAME} v{BRANCH_VERSION}")
    print(f"📚 Capabilities: {', '.join(CAPABILITIES)}")
    print(f"🔗 Endpoints: {len(ENDPOINTS)} mapped")
    print("🎓 Memory system is ready for retention and reflection.")
    return True

def status_check():
    """Optional status test for external probes."""
    return { "status": "active", "module": BRANCH_NAME, "version": BRANCH_VERSION }

__all__ = ["memory_api", "get_branch_info", "initialize_branch", "status_check"]
