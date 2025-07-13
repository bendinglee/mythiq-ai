from .routes import tuner_api

BRANCH_NAME = "Self Tuner"
BRANCH_VERSION = "1.0.0"

def initialize_branch():
    print(f"🧠 Initializing {BRANCH_NAME} v{BRANCH_VERSION}")
    return {
        "name": BRANCH_NAME,
        "version": BRANCH_VERSION,
        "route": "/api/self-tune",
        "status": "initialized"
    }

__all__ = ["tuner_api", "initialize_branch"]
