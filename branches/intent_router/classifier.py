import json
import os
from flask import jsonify

RULES_PATH = os.path.join(os.path.dirname(__file__), "rules.json")

def classify_intent(request):
    query = request.args.get("q", "").lower()

    try:
        with open(RULES_PATH, "r", encoding="utf-8") as f:
            rules = json.load(f)

        for label, keywords in rules.items():
            if any(word in query for word in keywords):
                return jsonify({"success": True, "intent": label})

        return jsonify({"success": True, "intent": "unknown"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
