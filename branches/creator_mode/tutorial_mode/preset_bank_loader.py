import json, os

PRESET_PATH = os.path.join(os.path.dirname(__file__), "../templates/chat_preset_bank.json")

def load_presets():
    if not os.path.exists(PRESET_PATH):
        return { "error": "Preset bank missing." }

    with open(PRESET_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("presets", [])
