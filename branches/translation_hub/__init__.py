from .routes import translation_api

BRANCH_NAME = "Translation Hub"
BRANCH_VERSION = "1.0.0"

def initialize_branch():
    print(f"🌍 Initializing {BRANCH_NAME} v{BRANCH_VERSION}")
    return {
        "name": BRANCH_NAME,
        "version": BRANCH_VERSION,
        "route": "/api/translate-text",
        "status": "initialized"
    }

__all__ = ["translation_api", "initialize_branch"]
