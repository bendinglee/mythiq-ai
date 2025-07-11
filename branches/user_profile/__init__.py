# 👤 Mythiq Branch: User Profile

from .routes import user_profile_api

BRANCH_NAME = "User Profile"
BRANCH_VERSION = "1.0.0"

def initialize_branch():
    print(f"👤 Initializing {BRANCH_NAME} v{BRANCH_VERSION}")
    return {
        "name": BRANCH_NAME,
        "version": BRANCH_VERSION,
        "route": "/api/user-profile",
        "status": "initialized"
    }

__all__ = ["user_profile_api", "initialize_branch"]
