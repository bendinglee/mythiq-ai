from flask import Blueprint, jsonify, request
from branches.interface_core.persona_state import get_current_profile
from branches.interface_core.intent_controller import update_intent_config
from branches.interface_core.intent_config import runtime_config

interface_api = Blueprint("interface_core", __name__)

@interface_api.route("/api/persona-status", methods=["GET"])
def persona_status():
    profile = get_current_profile(runtime_config.get("active_preset", "default"))
    return jsonify({
        "preset": runtime_config["active_preset"],
        "tone": profile.get("tone"),
        "style": profile.get("style"),
        "simplify": profile.get("simplify"),
        "overrides": runtime_config.get("plugin_overrides", [])
    })

@interface_api.route("/api/intent-ui", methods=["POST"])
def update_ui():
    updates = update_intent_config(request.get_json())
    return jsonify({ "success": True, "updated": updates })
