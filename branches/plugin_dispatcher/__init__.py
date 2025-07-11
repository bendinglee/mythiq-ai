# 🔌 Branch: Plugin Dispatcher

from .routes import plugin_api

BRANCH_NAME = "Plugin Dispatcher"
BRANCH_VERSION = "1.0.0"

def initialize_branch():
    print(f"🔌 Initializing {BRANCH_NAME} v{BRANCH_VERSION}")
    return {
        "name": BRANCH_NAME,
        "version": BRANCH_VERSION,
        "route": "/api/load-plugin",
        "status": "initialized"
    }

__all__ = ["plugin_api", "initialize_branch"]
