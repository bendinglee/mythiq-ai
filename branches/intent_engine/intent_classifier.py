import json, os

MAP_PATH = os.path.join(os.path.dirname(__file__), "intent_map.json")

def load_map():
    with open(MAP_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def classify_intent(user_input):
    input_lower = user_input.lower()
    intent_map = load_map()

    for entry in intent_map:
        for keyword in entry["keywords"]:
            if keyword in input_lower:
                return {
                    "intent": entry["intent"],
                    "confidence": 0.9,
                    "source": keyword
                }

    return {
        "intent": "general_knowledge",
        "confidence": 0.4,
        "source": "default"
    }
