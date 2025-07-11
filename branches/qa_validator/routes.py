from flask import Blueprint, request, jsonify
from branches.qa_validator.scorer import score_response
from branches.qa_validator.gradebook import log_grade

qa_api = Blueprint("qa_validator", __name__)

@qa_api.route("/api/qa-grade", methods=["POST"])
def grade_answer():
    """Original route for direct QA grading."""
    try:
        payload = request.get_json()
        if not payload.get("input") or not payload.get("output"):
            return jsonify({ "success": False, "error": "Missing input or output." }), 400

        result = score_response(payload)
        log_grade(payload, result)

        return jsonify({ "success": True, **result })
    except Exception as e:
        return jsonify({ "success": False, "error": str(e) }), 500

@qa_api.route("/api/validate-answer", methods=["POST"])
def validate_answer_route():
    """Required for orchestrator and fallback-safe injection."""
    return grade_answer()
