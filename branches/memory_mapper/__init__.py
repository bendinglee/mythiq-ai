from .routes import memory_mapper_api

BRANCH_NAME = "Memory Mapper"
BRANCH_VERSION = "1.0.0"

def initialize_branch():
    print(f"🧠 Initializing {BRANCH_NAME} v{BRANCH_VERSION}")
    return {
        "name": BRANCH_NAME,
        "version": BRANCH_VERSION,
        "route": "/api/memory-map",
        "status": "initialized"
    }

__all__ = ["memory_mapper_api", "initialize_branch"]
