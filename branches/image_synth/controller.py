from flask import request, jsonify
from .engine import generate_image_from_prompt
from .memory_writer import save_image_log

def synthesize_image_route():
    data = request.get_json()
    prompt = data.get("prompt", "").strip()

    if not prompt:
        return jsonify({"success": False, "error": "No prompt provided."}), 400

    try:
        image_url = generate_image_from_prompt(prompt)
        save_image_log(prompt, image_url)
        return jsonify({
            "success": True,
            "prompt": prompt,
            "image_url": image_url
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
