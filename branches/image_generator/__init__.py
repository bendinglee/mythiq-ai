from .routes import generate_image_route

BRANCH_NAME = "Image Generator"
BRANCH_VERSION = "1.0.0"

def initialize_branch():
    print(f"🎨 Initializing {BRANCH_NAME} v{BRANCH_VERSION}")
    return True

__all__ = ["generate_image_route", "initialize_branch"]
