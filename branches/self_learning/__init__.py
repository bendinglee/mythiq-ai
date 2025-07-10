from .routes import self_learning_api

BRANCH_NAME = "Self Learning"
BRANCH_VERSION = "1.0.0"

def initialize_branch():
    print(f"🧠 Booting {BRANCH_NAME} v{BRANCH_VERSION}")
    return True

__all__ = ["self_learning_api", "initialize_branch"]
