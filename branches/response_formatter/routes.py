from flask import Blueprint, request, jsonify
from branches.response_formatter.style_selector import select_style
from branches.response_formatter.tone_engine import apply_tone
from branches.response_formatter.prompt_simplifier import simplify_prompt

formatter_api = Blueprint("response_formatter", __name__)

@formatter_api.route("/api/format-response", methods=["POST"])
def format_response():
    try:
        data = request.get_json()
        raw_output = data.get("output", "").strip()
        style = data.get("style", "default")
        tone = data.get("tone", "friendly")
        simplify = data.get("simplify", False)

        if not raw_output:
            return jsonify({ "success": False, "error": "Missing output text." }), 400

        styled = select_style(raw_output, style)
        toned = apply_tone(styled, tone)
        if simplify:
            toned = simplify_prompt(toned)

        return jsonify({ "success": True, "formatted": toned })

    except Exception as e:
        return jsonify({ "success": False, "error": str(e) }), 500
