# 🧠 Mythiq Branch: Tutorial Mode

from .routes import tutorial_api

BRANCH_NAME = "Tutorial Mode"
BRANCH_VERSION = "1.0.0"

def initialize_branch():
    print(f"📘 Initializing {BRANCH_NAME} v{BRANCH_VERSION}")
    return {
        "name": BRANCH_NAME,
        "version": BRANCH_VERSION,
        "route": "/tutorial-mode",
        "status": "initialized"
    }

__all__ = ["tutorial_api", "initialize_branch"]
