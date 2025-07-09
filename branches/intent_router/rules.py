import json, os

RULE_PATH = os.path.join(os.path.dirname(__file__), "rules.json")

def load_route_rules():
    with open(RULE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
