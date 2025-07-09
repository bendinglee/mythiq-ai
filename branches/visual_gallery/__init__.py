from .routes import gallery_api

BRANCH_NAME = "Visual Gallery"
BRANCH_VERSION = "1.0.0"
BRANCH_DESCRIPTION = "Renders image logs as HTML gallery and JSON endpoint"

ENDPOINTS = [
    {"path": "/gallery", "method": "GET", "description": "Image gallery view"},
    {"path": "/api/gallery", "method": "GET", "description": "JSON image log feed"}
]

def get_branch_info():
    return {
        "name": BRANCH_NAME,
        "version": BRANCH_VERSION,
        "description": BRANCH_DESCRIPTION,
        "endpoints": ENDPOINTS,
        "status": "active"
    }

def initialize_branch():
    print(f"🖼️ Initializing {BRANCH_NAME} v{BRANCH_VERSION}")
    return True

__all__ = ["gallery_api", "get_branch_info", "initialize_branch"]
