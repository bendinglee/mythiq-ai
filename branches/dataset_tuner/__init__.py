# 📚 Branch: Dataset Tuner

from .routes import dataset_api

BRANCH_NAME = "Dataset Tuner"
BRANCH_VERSION = "1.0.0"

def initialize_branch():
    print(f"📚 Initializing {BRANCH_NAME} v{BRANCH_VERSION}")
    return {
        "name": BRANCH_NAME,
        "version": BRANCH_VERSION,
        "route": "/api/import-dataset",
        "status": "initialized"
    }

__all__ = ["dataset_api", "initialize_branch"]
