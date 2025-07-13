def reroute(task, reason="low diagnostics"):
    fallback_map = {
        "image_synth": "creator_mode",
        "video_generator": "visual_creator",
        "math_solver": "semantic_search"
    }
    return { "fallback": fallback_map.get(task, "core_router"), "reason": reason }
