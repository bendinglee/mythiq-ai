def score_response(entry):
    input_text = entry.get("input", "").lower()
    output_text = entry.get("output", "").lower()

    score = 0.0
    feedback = []

    if any(kw in output_text for kw in ["correct", "accurate", "true"]):
        score += 0.3
        feedback.append("✅ Appears factually accurate.")

    if len(output_text) > 80:
        score += 0.2
        feedback.append("🧠 Response length is appropriate.")

    if "i don't know" in output_text or "unsure":
        score -= 0.2
        feedback.append("⚠️ Uncertainty detected.")

    if "thank you" in output_text or "you’re welcome" in output_text:
        score += 0.1
        feedback.append("🙂 Friendly tone detected.")

    score += min(0.4, len(entry.get("tags", [])) * 0.05)

    return {
        "score": round(score, 2),
        "feedback": feedback,
        "tags": entry.get("tags", [])
    }
