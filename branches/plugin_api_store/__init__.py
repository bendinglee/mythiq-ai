# 🔌 Branch: Plugin API Store

from .routes import plugin_store_api

BRANCH_NAME = "Plugin API Store"
BRANCH_VERSION = "1.0.0"

def initialize_branch():
    print(f"🛠️ Initializing {BRANCH_NAME} v{BRANCH_VERSION}")
    return {
        "name": BRANCH_NAME,
        "version": BRANCH_VERSION,
        "route": "/api/plugin-store",
        "status": "initialized"
    }

__all__ = ["plugin_store_api", "initialize_branch"]
