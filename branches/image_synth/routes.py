from flask import Blueprint, request, jsonify
from branches.image_synth.controller import process_image_synthesis
from branches.image_synth.gallery_writer import archive_image
from branches.image_synth.memory_writer import log_synth_output
import json, os

image_api = Blueprint("image_synth", __name__)

@image_api.route("/api/synthesize-image", methods=["POST"])
def synth_image():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "").strip()
        modifiers = data.get("modifiers", [])

        if not prompt:
            return jsonify({ "success": False, "error": "Prompt is required." }), 400

        result = process_image_synthesis(prompt, modifiers)

        if result.get("success"):
            archive_image(result)

        return jsonify(result)

    except Exception as e:
        return jsonify({ "success": False, "error": str(e) }), 500

@image_api.route("/api/synthesize-preview", methods=["POST"])
def preview_prompt():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "")
        style = (data.get("modifiers") or ["default"])[0]

        preview = {
            "prompt": prompt,
            "style_applied": style,
            "estimated_tags": ["enhanced", style],
            "modifier_hint": f"This will apply '{style}' style transformation."
        }

        return jsonify({ "success": True, "preview": preview })

    except Exception as e:
        return jsonify({ "success": False, "error": str(e) }), 500

@image_api.route("/api/synthesize-batch", methods=["POST"])
def synth_batch():
    try:
        data = request.get_json()
        prompts = data.get("prompts", [])
        modifiers = data.get("modifiers", [])

        if not prompts or not isinstance(prompts, list):
            return jsonify({ "success": False, "error": "Missing or invalid prompts list." }), 400

        results = []
        for prompt in prompts:
            result = process_image_synthesis(prompt, modifiers)
            if result.get("success"):
                archive_image(result)
            results.append(result)

        return jsonify({ "success": True, "batch": results })

    except Exception as e:
        return jsonify({ "success": False, "error": str(e) }), 500

@image_api.route("/api/synthesize-status", methods=["GET"])
def synth_status():
    try:
        from branches.image_synth.memory_writer import LOG_PATH
        if not os.path.exists(LOG_PATH):
            return jsonify({ "success": True, "logs": [] })

        with open(LOG_PATH, "r") as f:
            logs = json.load(f)

        return jsonify({ "success": True, "logs": logs[-10:] })

    except Exception as e:
        return jsonify({ "success": False, "error": str(e) }), 500
