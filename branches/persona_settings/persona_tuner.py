import json, os

PRESET_PATH = os.path.join(os.path.dirname(__file__), "preset_profiles.json")

def load_presets():
    with open(PRESET_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def apply_persona_tuning(text, profile_name):
    presets = load_presets()
    config = presets.get(profile_name, presets.get("default", {}))
    tone = config.get("tone", "")
    simplify = config.get("simplify", False)
    style = config.get("style", "")

    tuned = text
    if tone == "friendly":
        tuned = f"😊 {tuned}"
    elif tone == "serious":
        tuned = f"🔍 {tuned}"
    elif tone == "excited":
        tuned = f"🎉 {tuned}"

    if simplify:
        tuned = tuned.replace("In summary,", "So").replace("Therefore,", "That means")

    if style == "bullet":
        tuned = "• " + "\n• ".join(tuned.split(". "))

    return tuned.strip()
