from flask import Blueprint, request, jsonify
from branches.persona_settings.persona_tuner import load_presets, apply_persona_tuning

persona_api = Blueprint("persona_settings", __name__)

@persona_api.route("/persona-settings", methods=["POST"])
def set_persona():
    try:
        data = request.get_json()
        selected = data.get("profile", "default")
        text = data.get("text", "")
        tuned = apply_persona_tuning(text, selected)
        return jsonify({ "success": True, "output": tuned, "profile": selected })
    except Exception as e:
        return jsonify({ "success": False, "error": str(e) })

@persona_api.route("/persona-presets", methods=["GET"])
def list_presets():
    return jsonify({ "success": True, "presets": list(load_presets().keys()) })
