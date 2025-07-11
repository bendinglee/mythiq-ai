def describe_visual(description):
    if not description:
        return { "success": False, "alt_text": "No visual description provided." }

    alt = f"🖼️ Alt Text: {description}"
    return { "success": True, "alt_text": alt }
