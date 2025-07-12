from flask import Blueprint, request, jsonify
from branches.creator_mode.creator_orchestrator import trigger_creation

creator_api = Blueprint("creator_mode", __name__)

@creator_api.route("/creator-mode", methods=["POST"])
def creator_mode():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "")
        mode = data.get("mode", "image")
        style = data.get("style", "default")

        if not prompt:
            return jsonify({ "success": False, "error": "Missing prompt." }), 400

        result = trigger_creation(prompt, mode, style)
        return jsonify(result)
    except Exception as e:
        return jsonify({ "success": False, "error": str(e) }), 500
