from branches.user_profile.profile_validator import validate_profile
from branches.user_profile.preference_engine import get_preferences

def test_profile():
    sample = {
        "preferred_tone": "friendly",
        "preferred_style": "highlight",
        "simplify_mode": True
    }
    valid, msg = validate_profile(sample)
    assert valid, f"❌ Validation failed: {msg}"

    prefs = get_preferences()
    assert "tone" in prefs and "style" in prefs, "❌ Preference parsing failed"

    print("✅ User profile test passed.")

if __name__ == "__main__":
    test_profile()
