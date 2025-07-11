from .routes import api_data_api

BRANCH_NAME = "API Integrator"
BRANCH_VERSION = "1.0.0"

def initialize_branch():
    print(f"🌐 Initializing {BRANCH_NAME} v{BRANCH_VERSION}")
    return {
        "name": BRANCH_NAME,
        "version": BRANCH_VERSION,
        "route": "/api/get-news",
        "status": "initialized"
    }

__all__ = ["api_data_api", "initialize_branch"]
