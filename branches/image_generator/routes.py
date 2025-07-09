from flask import request, jsonify
from branches.image_generator.generate import generate_image_from_prompt
from branches.image_generator.prompt_crafter import stylize_prompt
from branches.image_generator.history_log import log_image_generation

def generate_image_route():
    try:
        # 🌟 Step 1: Parse input
        data = request.get_json()
        raw_prompt = data.get("prompt", "").strip()
        style = data.get("style", "").strip() or "cinematic"

        if not raw_prompt:
            return jsonify({
                "success": False,
                "error": "No prompt provided."
            }), 400

        # 🎨 Step 2: Craft stylized prompt
        final_prompt = stylize_prompt(raw_prompt, style)

        # 🖼 Step 3: Generate image
        image_url = generate_image_from_prompt(final_prompt)

        # 🧠 Step 4: Log image data to memory
        log_image_generation(
            raw_prompt=raw_prompt,
            crafted_prompt=final_prompt,
            style=style,
            image_url=image_url
        )

        # ✅ Step 5: Return structured JSON
        return jsonify({
            "success": True,
            "prompt": final_prompt,
            "image_url": image_url
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
