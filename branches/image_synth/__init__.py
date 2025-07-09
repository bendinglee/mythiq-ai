from .routes import synth_image_route

BRANCH_NAME = "Image Synthesizer"
BRANCH_VERSION = "1.0.0"

def initialize_branch():
    print(f"🖼️ Initializing {BRANCH_NAME} v{BRANCH_VERSION}")
    return True

__all__ = ["synth_image_route", "initialize_branch"]
