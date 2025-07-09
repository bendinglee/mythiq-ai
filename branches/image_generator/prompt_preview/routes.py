from flask import request, jsonify
from branches.image_generator.prompt_preview.preview_engine import generate_prompt_preview

def preview_prompt_route():
    try:
        data = request.get_json()
        raw_prompt = data.get("prompt", "").strip()
        style = data.get("style", "").strip() or "cinematic"

        if not raw_prompt:
            return jsonify({ "success": False, "error": "Missing prompt." }), 400

        preview = generate_prompt_preview(raw_prompt, style)
        return jsonify({ "success": True, "preview": preview })

    except Exception as e:
        return jsonify({ "success": False, "error": str(e) }), 500
