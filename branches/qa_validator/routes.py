from flask import Blueprint, request, jsonify
import time

from branches.qa_validator.scorer import score_response
from branches.qa_validator.gradebook import log_grade
from branches.self_learning.score_feedback_loop import feedback_loop

qa_api = Blueprint("qa_validator", __name__)

@qa_api.route("/api/qa-grade", methods=["POST"])
def grade_answer():
    """Direct QA grading for input-output pairs."""
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
    """Fallback-safe injection route used by orchestration."""
    return grade_answer()

@qa_api.route("/api/grade-feedback", methods=["POST"])
def full_feedback_pipeline():
    """Enriched feedback scoring with self-learning enhancements."""
    try:
        payload = request.get_json()
        enriched = feedback_loop(payload)
        return jsonify({ "success": True, "enriched": enriched })
    except Exception as e:
        return jsonify({ "success": False, "error": str(e) }), 500

@qa_api.route("/api/status", methods=["GET"])
def status_check():
    """Healthcheck route used by Railway and monitoring systems."""
    return jsonify({
        "status": "ok",
        "module": "qa_validator",
        "timestamp": time.time()
    })
