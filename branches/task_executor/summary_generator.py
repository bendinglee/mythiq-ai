def summarize_text(text, style="default"):
    if not text:
        return { "success": False, "message": "No input to summarize." }

    # Simulated logic (replace with NLP model later)
    lines = [line.strip() for line in text.split(".") if len(line.strip()) > 5]
    summary = lines[:3]

    if style == "bullet":
        formatted = ["• " + line for line in summary]
    elif style == "highlight":
        formatted = ["🔍 " + line for line in summary]
    else:
        formatted = summary

    return {
        "success": True,
        "summary": formatted,
        "style": style
    }
