import json
import os
from flask import request, jsonify
from branches.uncertainty_detector.analyzer import assess_uncertainty
from branches.intent_router.simulator import simulate_preview_response  # Optional stub

RULES_PATH = os.path.join(os.path.dirname(__file__), "rules.json")

def classify_intent(request):
    query = request.args.get("q", "") or request.get_json().get("input", "")
    query = query.lower()

    try:
        # Load intent rules
        with open(RULES_PATH, "r", encoding="utf-8") as f:
            rules = json.load(f)

        intent = "unknown"
        for label, keywords in rules.items():
            if any(word in query for word in keywords):
                intent = label
                break

        # Optionally simulate response and assess confidence
        simulated = simulate_preview_response(intent, query)  # Optional stub logic
        uncertainty = assess_uncertainty(simulated)

        return jsonify({
            "success": True,
            "intent": intent,
            "uncertainty": uncertainty["is_uncertain"],
            "confidence": uncertainty["confidence_score"],
            "source": "intent_router"
        })

    except Exception as e:
        return jsonify({ "success": False, "error": str(e) }), 500
