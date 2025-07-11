from flask import Blueprint, request, jsonify
from branches.accessibility_core.voice_captioner import generate_voice_caption
from branches.accessibility_core.alt_text_generator import describe_visual
from branches.accessibility_core.screenreader_adapter import format_for_screen_reader

accessibility_api = Blueprint("accessibility_core", __name__)

@accessibility_api.route("/api/accessibility/voice-caption", methods=["POST"])
def voice_caption():
    data = request.get_json()
    text = data.get("text", "").strip()
    result = generate_voice_caption(text)
    return jsonify(result)

@accessibility_api.route("/api/accessibility/alt-text", methods=["POST"])
def alt_text():
    data = request.get_json()
    image_description = data.get("description", "").strip()
    result = describe_visual(image_description)
    return jsonify(result)

@accessibility_api.route("/api/accessibility/screen-reader", methods=["POST"])
def screen_reader_format():
    data = request.get_json()
    output = data.get("output", "").strip()
    result = format_for_screen_reader(output)
    return jsonify(result)
