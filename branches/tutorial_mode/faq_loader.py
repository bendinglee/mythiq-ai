import json, os

GUIDE_PATH = os.path.join(os.path.dirname(__file__), "../user_profile/tutorial_guide.json")

def load_faq():
    if not os.path.exists(GUIDE_PATH):
        return { "error": "Tutorial guide not found." }

    with open(GUIDE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
