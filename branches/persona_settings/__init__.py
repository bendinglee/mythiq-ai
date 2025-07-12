# 👤 Mythiq Branch: Persona Settings

from .routes import persona_api

BRANCH_NAME = "Persona Settings"
BRANCH_VERSION = "1.0.0"

def initialize_branch():
    print(f"🎭 Initializing {BRANCH_NAME} v{BRANCH_VERSION}")
    return {
        "name": BRANCH_NAME,
        "version": BRANCH_VERSION,
        "route": "/persona-settings",
        "status": "initialized"
    }

__all__ = ["persona_api", "initialize_branch"]
