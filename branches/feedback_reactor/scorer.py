def score_feedback_entry(entry):
    score = 0.0
    if entry.get("confidence") < 0.5: score += 0.4
    if "error" in entry.get("user_feedback", "").lower(): score += 0.3
    if entry.get("tags"): score += min(0.2, len(entry["tags"]) * 0.05)
    return round(score, 2)
