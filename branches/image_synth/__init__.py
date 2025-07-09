from .routes import image_api

BRANCH_NAME = "Image Synth"
BRANCH_VERSION = "1.0.0"
BRANCH_DESCRIPTION = "Image generation using Stable Diffusion"

CAPABILITIES = ["image_generation", "prompt_translation", "memory_logging"]

ENDPOINTS = [
    {"path": "/api/synthesize-image", "method": "POST", "description": "Generate image from prompt"}
]

def get_branch_info():
    return {
        "name": BRANCH_NAME,
        "version": BRANCH_VERSION,
        "description": BRANCH_DESCRIPTION,
        "capabilities": CAPABILITIES,
        "endpoints": ENDPOINTS,
        "status": "active"
    }

def initialize_branch():
    print(f"🎨 Booting {BRANCH_NAME} v{BRANCH_VERSION}")
    return True

__all__ = ["image_api", "get_branch_info", "initialize_branch"]
