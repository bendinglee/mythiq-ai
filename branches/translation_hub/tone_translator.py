def rewrite_tone(text, tone):
    if tone == "excited":
        return f"🎉 Awesome! {text}"
    elif tone == "formal":
        return f"In summary: {text}"
    elif tone == "curious":
        return f"Have you considered? {text}"
    elif tone == "friendly":
        return f"😊 Here's something for you: {text}"
    else:
        return text
