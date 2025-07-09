def score_memory_entry(entry):
    score = 0.0
    meta = entry.get("meta", {})
    tags = entry.get("tags", [])

    # ✅ Score based on success
    if entry.get("success") is True:
        score += 0.5

    # 📊 Add reflection weight if present
    reflection_weight = meta.get("reflection_weight", 0.0)
    if isinstance(reflection_weight, (float, int)):
        score += min(0.3, reflection_weight)  # Cap reflection bonus

    # 🧠 Tag-based weighting
    if tags:
        score += min(0.3, len(tags) * 0.05)

        # Bonus for critical tag
        if "critical" in [t.lower() for t in tags]:
            score += 0.2

    # 📚 Input length bonus
    input_text = entry.get("input", "")
    if isinstance(input_text, str) and len(input_text) > 30:
        score += 0.1

    return round(score, 2)
