def confidence_score(request, return_only=False):
    input_text = request.get("input", "")
    output_text = request.get("output", "")
    # Simulated scoring — replace with real NLP uncertainty if needed
    score = 1.0 if "I don't know" not in output_text.lower() else 0.4
    result = { "confidence": round(score, 2) }

    if return_only:
        return result

    return { "success": True, **result }
