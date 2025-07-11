def select_style(text, style):
    style_map = {
        "default": text,
        "bullet": "\n• " + "\n• ".join(text.split(". ")),
        "formal": f"In conclusion, {text}",
        "highlight": f"🔍 Here's what you need to know: {text}",
        "beginner": f"Let’s break it down: {text}"
    }
    return style_map.get(style, text)
