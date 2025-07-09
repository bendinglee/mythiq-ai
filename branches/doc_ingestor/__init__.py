from .routes import ingestor_api

BRANCH_NAME = "Document Ingestor"
BRANCH_VERSION = "1.0.0"
BRANCH_DESCRIPTION = "Parse, vectorize, and store knowledge from external documents"

def initialize_branch():
    print(f"📚 Initializing {BRANCH_NAME} v{BRANCH_VERSION}")
    return True

__all__ = ["ingestor_api", "initialize_branch"]
