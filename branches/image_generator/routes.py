from flask import request, jsonify
from branches.image_generator.generate import generate_image_from_prompt
from branches.image_generator.prompt_crafter import stylize_prompt
from branches.image_generator.history_log import log_image_generation

def generate_image_route():
    try:
        data = request.get_json()
        raw_prompt = data.get("prompt", "").strip()
        style = data.get("style", "").strip() or "cinematic"

        if not raw_prompt:
            return jsonify({ "success": False, "error": "No prompt provided." }), 400

        final_prompt = stylize_prompt(raw_prompt, style)
        image_url = generate_image_from_prompt(final_prompt)

        log_image_generation(raw_prompt, final_prompt, style, image_url)

        return jsonify({
            "success": True,
            "prompt": final_prompt,
            "image_url": image_url
        })

    except Exception as e:
        return jsonify({ "success": False, "error": str(e) }), 500
