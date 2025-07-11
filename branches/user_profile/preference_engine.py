from branches.user_profile.profile_manager import load_profile

def get_preferences():
    raw = load_profile().get("profile", {})
    tone = raw.get("preferred_tone", "friendly")
    style = raw.get("preferred_style", "default")
    simplify = raw.get("simplify_mode", False)

    return {
        "tone": tone,
        "style": style,
        "simplify_mode": simplify
    }
