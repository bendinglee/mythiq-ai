from flask import Blueprint, request, jsonify
from branches.intent_router.router import route_input
from branches.intent_router.fallback import fallback_to_uncertainty

intent_api = Blueprint("intent_router", __name__)

@intent_api.route("/api/intent-route", methods=["POST"])
def intent_route():
    try:
        data = request.get_json()
        text = data.get("text", "").strip()

        if not text:
            return jsonify({ "success": False, "error": "No input provided." }), 400

        result = route_input(text)

        if result["confidence"] < 0.5:
            return jsonify(fallback_to_uncertainty(text))

        return jsonify({ "success": True, **result })

    except Exception as e:
        return jsonify({ "success": False, "error": str(e) }), 500
