def annotate_emotion(text):
    if "hate" in text.lower():
        return "😡 Angry"
    elif "love" in text.lower():
        return "❤️ Positive"
    elif "confused" in text.lower():
        return "🤔 Uncertain"
    else:
        return "🙂 Neutral"
