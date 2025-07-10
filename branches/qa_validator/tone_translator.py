def translate_tone(text, tone="playful"):
    if tone == "playful":
        return f"🎉 Just so you know: {text}"
    elif tone == "curious":
        return f"🤔 Did you realize? {text}"
    elif tone == "serious":
        return f"Let’s be direct: {text}"
    else:
        return text
