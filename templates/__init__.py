from .routes import templates_api

BRANCH_NAME = "Templates"
BRANCH_VERSION = "1.0.0"

def initialize_branch():
    print(f"🗂️ Initializing {BRANCH_NAME} v{BRANCH_VERSION}")
    return {
        "name": BRANCH_NAME,
        "version": BRANCH_VERSION,
        "route": "/api/templates",
        "status": "initialized"
    }

__all__ = ["templates_api", "initialize_branch"]
