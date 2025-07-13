def tag(text):
    if "love" in text: return "positive"
    elif "hate" in text: return "negative"
    elif "confused" in text: return "uncertain"
    return "neutral"
