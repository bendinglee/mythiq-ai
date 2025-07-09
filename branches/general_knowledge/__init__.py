from .routes import knowledge_api

BRANCH_NAME = "General Knowledge"
BRANCH_VERSION = "1.0.0"
BRANCH_DESCRIPTION = "Answers factual questions based on JSON modules"

def initialize_branch():
    print(f"📖 Initializing {BRANCH_NAME} v{BRANCH_VERSION}")
    return True

__all__ = ["knowledge_api", "initialize_branch"]
