from .routes import plugin_constructor_api

BRANCH_NAME = "Plugin Constructor"
BRANCH_VERSION = "1.0.0"

def initialize_branch():
    print(f"🧠 Initializing {BRANCH_NAME} v{BRANCH_VERSION}")
    return {
        "name": BRANCH_NAME,
        "version": BRANCH_VERSION,
        "route": "/api/plugin-construct",
        "status": "initialized"
    }

__all__ = ["plugin_constructor_api", "initialize_branch"]
