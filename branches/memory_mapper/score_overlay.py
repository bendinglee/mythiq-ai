def score_tags(meta):
    return {
        "score": round(meta.get("score", 0.0), 2),
        "confidence": round(meta.get("confidence", 0.0), 2),
        "diagnostic_score": round(meta.get("diagnostic_score", 0.0), 2)
    }
