def overlay_confidence(text, score):
    if score < 0.3:
        return f"⚠️ LOW CONFIDENCE: {text}"
    elif score < 0.7:
        return f"🧠 MODERATE CONFIDENCE: {text}"
    else:
        return f"✅ CONFIDENT: {text}"
