from .routes import uncertainty_api

BRANCH_NAME = "Uncertainty Detector"
BRANCH_VERSION = "1.0.0"

def initialize_branch():
    print(f"🚦 Initializing {BRANCH_NAME} v{BRANCH_VERSION}")
    return True

__all__ = ["uncertainty_api", "initialize_branch"]
