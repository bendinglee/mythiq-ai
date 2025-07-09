from .routes import qa_api

BRANCH_NAME = "QA Validator"
BRANCH_VERSION = "1.0.0"

def initialize_branch():
    print(f"🔍 Initializing {BRANCH_NAME} v{BRANCH_VERSION}")
    return True

__all__ = ["qa_api", "initialize_branch"]
