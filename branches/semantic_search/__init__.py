from .query_router import semantic_query_route

BRANCH_NAME = "Semantic Search"
BRANCH_VERSION = "1.0.0"

def initialize_branch():
    print(f"🔎 Booting {BRANCH_NAME} v{BRANCH_VERSION}")
    return True

__all__ = ["semantic_query_route", "initialize_branch"]
