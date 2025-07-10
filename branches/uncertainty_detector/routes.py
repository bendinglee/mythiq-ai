from flask import Blueprint, request, jsonify
from branches.uncertainty_detector.analyzer import detect_uncertain_phrases
from branches.uncertainty_detector.confidence_grader import grade_confidence
from branches.uncertainty_detector.uncertainty_reporter import build_report

uncertainty_api = Blueprint("uncertainty_detector", __name__)

@uncertainty_api.route("/api/uncertainty-check", methods=["POST"])
def check_uncertainty():
    try:
        data = request.get_json()
        content = data.get("content", "").strip()

        if not content:
            return jsonify({
                "success": False,
                "error": "Missing or empty content field."
            }), 400

        phrases = detect_uncertain_phrases(content)
        score = grade_confidence(content, phrases)
        report = build_report(content, phrases, score)

        return jsonify({
            "success": True,
            "score": score,
            "phrases": phrases,
            "report": report
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Uncertainty analysis failed: {str(e)}"
        }), 500
