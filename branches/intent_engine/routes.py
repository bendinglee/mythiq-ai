from flask import Blueprint, request, jsonify
from branches.intent_engine.intent_classifier import classify_intent
from branches.intent_engine.intent_resolver import resolve_intent
from branches.intent_engine.intent_logger import log_intent

intent_api = Blueprint("intent_engine", __name__)

@intent_api.route("/api/parse-intent", methods=["POST"])
def parse_intent():
    try:
        data = request.get_json()
        user_input = data.get("input", "").strip()

        if not user_input:
            return jsonify({ "success": False, "error": "Missing input." }), 400

        prediction = classify_intent(user_input)
        resolved = resolve_intent(prediction)
        log_intent(user_input, resolved)

        return jsonify({ "success": True, "intent": resolved })
    except Exception as e:
        return jsonify({ "success": False, "error": str(e) }), 500
