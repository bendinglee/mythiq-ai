import json, os
PRESET_PATH = "branches/persona_settings/preset_profiles.json"

def get_current_profile(preset="default"):
    if not os.path.exists(PRESET_PATH): return {}
    with open(PRESET_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get(preset, {})
