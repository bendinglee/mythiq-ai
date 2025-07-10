from .routes import seo_api

BRANCH_NAME = "SEO Master"
BRANCH_VERSION = "1.0.0"

def initialize_branch():
    print(f"📈 Initializing {BRANCH_NAME} v{BRANCH_VERSION}")
    return True

__all__ = ["seo_api", "initialize_branch"]
