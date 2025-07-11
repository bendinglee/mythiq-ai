def format_for_screen_reader(text):
    if not text:
        return { "success": False, "formatted": "" }

    # Simulated screen-reader markup
    formatted = f"<sr-output aria-label='Output'>{text}</sr-output>"
    return { "success": True, "formatted": formatted }
