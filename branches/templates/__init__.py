from .routes import core_router_api
from branches import (
    math_solver, memory_core, qa_validator, self_learning,
    semantic_search, seo_master, image_generator, image_synth,
    intent_router, general_knowledge, doc_ingestor, uncertainty_detector
)

BRANCH_NAME = "Core Router"
BRANCH_VERSION = "1.0.0"

def initialize_branch():
    print(f"🧠 Mythiq Core Orchestrator Online [{BRANCH_VERSION}]")
    branches = [
        math_solver, memory_core, qa_validator, self_learning,
        semantic_search, seo_master, image_generator, image_synth,
        intent_router, general_knowledge, doc_ingestor, uncertainty_detector
    ]
    for b in branches:
        if hasattr(b, "initialize_branch"):
            b.initialize_branch()
    return True

__all__ = ["core_router_api", "initialize_branch"]
