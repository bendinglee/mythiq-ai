from flask import Blueprint, request, jsonify
from branches.video_generator.controller import generate_video_clip

video_api = Blueprint("video_generator", __name__)

@video_api.route("/api/generate-video", methods=["POST"])
def generate_video():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "").strip()
        style = data.get("style", "cinematic")
        duration = int(data.get("duration", 5))

        if not prompt:
            return jsonify({ "success": False, "error": "Missing prompt." }), 400

        result = generate_video_clip(prompt, style, duration)
        return jsonify(result)
    except Exception as e:
        return jsonify({ "success": False, "error": str(e) }), 500
