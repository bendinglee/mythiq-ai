def annotate_emotion(text):
    keywords = {
        "love": "positive",
        "hate": "negative",
        "confused": "uncertain",
        "awesome": "excited",
        "bored": "neutral"
    }
    tag = "neutral"
    for key, value in keywords.items():
        if key in text.lower():
            tag = value
            break
    return { "emotion_tag": tag }
