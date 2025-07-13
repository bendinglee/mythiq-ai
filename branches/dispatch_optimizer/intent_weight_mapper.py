def map_intent_to_task(intent, confidence, diag_score, plugins):
    if diag_score < 0.4:
        return "fallback_safe_mode"
    
    if "creator" in intent and "visual_creator" in plugins:
        return "visual_creator_pipeline"
    elif "video" in intent and "video_generator" in plugins:
        return "video_generation"
    elif "math" in intent:
        return "math_solver"
    elif confidence < 0.5:
        return "semantic_search"
    else:
        return "core_dispatch"
