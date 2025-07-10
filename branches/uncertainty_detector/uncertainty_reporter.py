def build_report(content, phrases, score):
    feedback = []

    if phrases:
        feedback.append(f"Detected {len(phrases)} hedging phrases.")
        feedback += [f"→ '{p}' is considered uncertain." for p in phrases]
    else:
        feedback.append("✅ No uncertainty patterns detected.")

    if score < 0.5:
        feedback.append("⚠️ Low confidence detected — consider strengthening claims.")
    elif score < 0.8:
        feedback.append("🧠 Moderate confidence — revise for clarity or precision.")
    else:
        feedback.append("✅ High-confidence output.")

    return feedback
