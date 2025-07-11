def validate_profile(data):
    allowed_tones = ["friendly", "serious", "excited", "curious", "formal"]
    allowed_styles = ["default", "highlight", "bullet", "formal", "beginner"]

    tone = data.get("preferred_tone", "friendly")
    style = data.get("preferred_style", "default")
    simplify = data.get("simplify_mode", False)

    if tone not in allowed_tones:
        return False, f"Invalid tone '{tone}'"
    if style not in allowed_styles:
        return False, f"Invalid style '{style}'"
    if not isinstance(simplify, bool):
        return False, "Simplify mode must be true/false"

    return True, "Valid"
