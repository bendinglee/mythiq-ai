from flask import Blueprint, jsonify, request
from branches.self_tuner.tune_persona import tune_persona_settings

tuner_api = Blueprint("self_tuner", __name__)

@tuner_api.route("/api/self-tune", methods=["POST"])
def self_tune():
    try:
        meta = request.get_json().get("meta", {})
        result = tune_persona_settings(meta)
        return jsonify({ "success": True, "updated": result })
    except Exception as e:
        return jsonify({ "success": False, "error": str(e) })
