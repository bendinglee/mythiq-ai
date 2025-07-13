import json, os

PRESET_PATH = os.path.join(os.path.dirname(__file__), "../persona_settings/preset_profiles.json")

def update_profile(name, tone=None, style=None, simplify=None):
    if not os.path.exists(PRESET_PATH):
        return { "error": "Preset file missing." }

    with open(PRESET_PATH, "r", encoding="utf-8") as f:
        profiles = json.load(f)

    if name not in profiles:
        profiles[name] = {}

    if tone is not None:
        profiles[name]["tone"] = tone
    if style is not None:
        profiles[name]["style"] = style
    if simplify is not None:
        profiles[name]["simplify"] = simplify

    with open(PRESET_PATH, "w", encoding="utf-8") as f:
        json.dump(profiles, f, indent=2)

    return profiles[name]
