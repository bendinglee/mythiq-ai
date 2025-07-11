from branches import (
    core_router, doc_ingestor, feedback_reactor, general_knowledge,
    image_generator, image_synth, intent_router, math_solver,
    memory_core, qa_validator, self_learning, semantic_search,
    seo_master, templates, tests, uncertainty_detector,
    vector_store, visual_creator, visual_gallery
)

ACTIVE_BRANCHES = [
    core_router, doc_ingestor, feedback_reactor, general_knowledge,
    image_generator, image_synth, intent_router, math_solver,
    memory_core, qa_validator, self_learning, semantic_search,
    seo_master, templates, tests, uncertainty_detector,
    vector_store, visual_creator, visual_gallery
]

def initialize_all_branches():
    initialized = []
    for branch in ACTIVE_BRANCHES:
        init_fn = getattr(branch, "initialize_branch", None)
        if callable(init_fn):
            result = init_fn()
            if result:
                initialized.append(result)
    return initialized
