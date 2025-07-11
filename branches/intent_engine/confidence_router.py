def reroute_low_confidence(prediction):
    fallback_map = {
        "general_knowledge": "semantic_search",
        "semantic_search": "memory_core",
        "default": "qa_validator"
    }
    fallback_intent = fallback_map.get(prediction["intent"], "general_knowledge")
    prediction["intent"] = fallback_intent
    prediction["confidence"] = 0.6
    prediction["source"] = "fallback"
    return prediction
