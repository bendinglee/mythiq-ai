from .routes import dispatch_optimizer_api

BRANCH_NAME = "Adaptive Dispatch"
BRANCH_VERSION = "1.0.0"

def initialize_branch():
    print(f"🧠 Initializing {BRANCH_NAME} v{BRANCH_VERSION}")
    return {
        "name": BRANCH_NAME,
        "version": BRANCH_VERSION,
        "route": "/api/dispatch-optimize",
        "status": "initialized"
    }

__all__ = ["dispatch_optimizer_api", "initialize_branch"]
