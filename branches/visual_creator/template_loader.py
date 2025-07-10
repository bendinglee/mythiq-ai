import json, os

def load_template(style):
    try:
        with open(os.path.join(os.path.dirname(__file__), "template_bank.json"), "r", encoding="utf-8") as f:
            bank = json.load(f)
            return next((t for t in bank if t["style"] == style), {})
    except Exception as e:
        print(f"[Template Loader] Failed to load template: {e}")
        return {}
