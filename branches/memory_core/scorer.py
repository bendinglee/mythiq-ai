def score_memory_entry(entry):
    score = 0.0
    if entry.get("success"): score += 0.5
    if "reflection_weight" in entry.get("meta", {}): score += entry["meta"]["reflection_weight"]
    if entry.get("tags"): score += min(0.3, len(entry["tags"]) * 0.05)
    if entry.get("input") and len(entry["input"]) > 30: score += 0.1
    return round(score, 2)
