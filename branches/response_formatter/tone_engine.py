def apply_tone(text, tone="friendly"):
    if tone == "friendly":
        return f"😊 Sure! {text}"
    elif tone == "curious":
        return f"🤔 Ever wondered? {text}"
    elif tone == "excited":
        return f"🎉 Great news! {text}"
    elif tone == "serious":
        return f"🔎 Precisely: {text}"
    else:
        return text
