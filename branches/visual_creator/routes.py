from flask import Blueprint, request, jsonify
from branches.visual_creator.controller import create_visual_asset

visual_api = Blueprint("visual_creator", __name__)

@visual_api.route("/api/create-visual", methods=["POST"])
def create_visual():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "").strip()
        style = data.get("style", "default")
        overlay = data.get("overlay", "")

        if not prompt:
            return jsonify({ "success": False, "error": "Missing prompt." }), 400

        result = create_visual_asset(prompt, style, overlay)
        return jsonify(result)
    except Exception as e:
        return jsonify({ "success": False, "error": str(e) }), 500
