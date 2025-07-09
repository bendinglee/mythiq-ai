from .routes import feedback_api

BRANCH_NAME = "Feedback Reactor"
BRANCH_VERSION = "1.0.0"

def initialize_branch():
    print(f"🧠 Feedback Reactor v{BRANCH_VERSION} initialized")
    return True

__all__ = ["feedback_api", "initialize_branch"]
