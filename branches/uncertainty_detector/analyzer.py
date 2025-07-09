def assess_uncertainty(response_obj):
    output = response_obj.get("output", "")
    confidence = response_obj.get("confidence", 1.0)

    # Define thresholds
    uncertain_phrases = ["I don't know", "not sure", "can't answer", "unknown", "no data"]
    low_confidence = confidence < 0.6

    matches_uncertain = any(p in output.lower() for p in uncertain_phrases)

    return {
        "is_uncertain": matches_uncertain or low_confidence,
        "confidence_score": confidence
    }
