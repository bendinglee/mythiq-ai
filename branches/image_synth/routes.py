from flask import Blueprint, request, jsonify
from branches.image_synth.controller import process_image_synthesis

image_api = Blueprint("image_synth", __name__)

@image_api.route("/api/synthesize-image", methods=["POST"])
def synth_image():
    try:
        # 📥 Parse request payload
        data = request.get_json()
        prompt = data.get("prompt", "").strip()
        modifiers = data.get("modifiers", [])

        if not prompt:
            return jsonify({ "success": False, "error": "Prompt is required." }), 400

        # 🧠 Delegate to controller
        result = process_image_synthesis(prompt, modifiers)
        return jsonify(result)

    except Exception as e:
        return jsonify({ "success": False, "error": str(e) }), 500
