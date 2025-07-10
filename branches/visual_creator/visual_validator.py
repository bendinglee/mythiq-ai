def validate_visual_request(prompt, style):
    if not isinstance(prompt, str) or len(prompt.strip()) < 5:
        return False, "⚠️ Prompt too short or invalid."
    allowed = ["default", "cyberpunk", "minimalist", "fantasy"]
    if style not in allowed:
        return False, f"⚠️ Unknown style '{style}'."
    return True, "Valid"
