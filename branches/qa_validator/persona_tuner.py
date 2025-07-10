def tune_output_style(text, style="friendly"):
    if style == "formal":
        return f"In summary, {text}"
    elif style == "playful":
        return f"🌟 Here’s the scoop: {text}"
    elif style == "socratic":
        return f"What do you think? Well, consider this: {text}"
    else:
        return text
