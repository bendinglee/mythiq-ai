# 📊 Mythiq Branch: QA Validator

from .routes import qa_api, validate_answer_route

BRANCH_NAME = "QA Validator"
BRANCH_VERSION = "1.0.0"

def initialize_branch():
    print(f"🔍 Initializing {BRANCH_NAME} v{BRANCH_VERSION}")
    return {
        "name": BRANCH_NAME,
        "version": BRANCH_VERSION,
        "status": "initialized",
        "route": "/api/validate-answer"
    }

__all__ = ["qa_api", "validate_answer_route", "initialize_branch"]
