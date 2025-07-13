from .routes import interface_api

BRANCH_NAME = "Interface Core"
BRANCH_VERSION = "1.0.0"

def initialize_branch():
    print(f"🧠 Initializing {BRANCH_NAME} v{BRANCH_VERSION}")
    return {
        "name": BRANCH_NAME,
        "version": BRANCH_VERSION,
        "route": "/api/persona-status",
        "status": "initialized"
    }

__all__ = ["interface_api", "initialize_branch"]
