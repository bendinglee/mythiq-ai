import json, os

PROFILE_PATH = os.path.join(os.path.dirname(__file__), "profile.json")

def load_profile():
    if not os.path.exists(PROFILE_PATH):
        return { "success": True, "profile": {} }
    with open(PROFILE_PATH, "r", encoding="utf-8") as f:
        return { "success": True, "profile": json.load(f) }

def update_profile(data):
    try:
        with open(PROFILE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return { "success": True, "message": "✅ Profile updated." }
    except Exception as e:
        return { "success": False, "error": f"Update failed: {str(e)}" }
