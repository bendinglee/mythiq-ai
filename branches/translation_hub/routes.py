from flask import Blueprint, request, jsonify
from branches.translation_hub.translator_engine import translate_text
from branches.translation_hub.tone_translator import rewrite_tone
from branches.translation_hub.translation_logger import log_translation

translation_api = Blueprint("translation_hub", __name__)

@translation_api.route("/api/translate-text", methods=["POST"])
def translate():
    try:
        data = request.get_json()
        input_text = data.get("text", "").strip()
        target_lang = data.get("lang", "en")
        tone = data.get("tone", "default")

        if not input_text:
            return jsonify({ "success": False, "error": "Missing input text." }), 400

        translation = translate_text(input_text, target_lang)
        toned = rewrite_tone(translation, tone)
        log_translation(input_text, toned, target_lang, tone)

        return jsonify({ "success": True, "translated": toned, "lang": target_lang, "tone": tone })
    except Exception as e:
        return jsonify({ "success": False, "error": str(e) }), 500
