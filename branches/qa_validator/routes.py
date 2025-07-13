from flask import Blueprint, request, jsonify
from branches.qa_validator.scorer import score_response
from branches.qa_validator.gradebook import log_grade

# New import for the feedback loop pipeline
from branches.self_learning.score_feedback_loop import feedback_loop

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

@qa_api.route("/api/grade-feedback", methods=["POST"])
def full_feedback_pipeline():
    """New route to process enriched feedback using the self-learning loop."""
    try:
        payload = request.get_json()
        enriched = feedback_loop(payload)
        return jsonify({ "success": True, "enriched": enriched })
    except Exception as e:
        return jsonify({ "success": False, "error": str(e) }), 500
