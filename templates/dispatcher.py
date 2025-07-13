import json, os

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "chat_preset_bank.json")

def load_templates():
    if not os.path.exists(TEMPLATE_PATH):
        return []
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("presets", [])
