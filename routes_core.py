from flask import Blueprint, request, jsonify
import time
from branches.qa_validator.scorer import score_response
from branches.qa_validator.gradebook import log_grade
from branches.self_learning.score_feedback_loop import feedback_loop
from branches.math_solver.solver import solve_math_query
from branches.reflex_trainer.emotion_tagger import tag
from branches.reflex_trainer.response_rewriter import rewrite
from branches.cortex_fusion.task_dispatcher import dispatch as dispatch_task
from branches.cortex_fusion.fallback_router import reroute
from branches.image_generator.routes import generate_image_route

core_api = Blueprint("core_api", __name__)

@core_api.route("/api/status", methods=["GET"])
def status_check():
    return jsonify({
        "status": "ok",
        "timestamp": time.time()
    })

@core_api.route("/api/qa-grade", methods=["POST"])
def grade_answer():
    try:
        payload = request.get_json()
        if not payload.get("input") or not payload.get("output"):
            return jsonify({ "success": False, "error": "Missing input or output." }), 400
        result = score_response(payload)
        log_grade(payload, result)
        return jsonify({ "success": True, **result })
    except Exception as e:
        return jsonify({ "success": False, "error": str(e) }), 500

@core_api.route("/api/validate-answer", methods=["POST"])
def validate_answer():
    return grade_answer()

@core_api.route("/api/grade-feedback", methods=["POST"])
def grade_feedback():
    try:
        payload = request.get_json()
        enriched = feedback_loop(payload)
        return jsonify({ "success": True, "enriched": enriched })
    except Exception as e:
        return jsonify({ "success": False, "error": str(e) }), 500

@core_api.route("/api/solve-math", methods=["POST"])
def solve_math():
    try:
        data = request.get_json()
        result = solve_math_query(data.get("question", ""))
        return jsonify({ "success": True, "result": result })
    except Exception as e:
        return jsonify({ "success": False, "error": str(e) }), 500

@core_api.route("/api/generate-image", methods=["POST"])
def generate_image():
    return generate_image_route()

@core_api.route("/api/dispatch-reflex", methods=["POST"])
def dispatch_reflex():
    try:
        payload = request.get_json()
        enriched = feedback_loop(payload)
        output_text = enriched.get("output", "")
        emotion = tag(output_text)
        rewritten = rewrite(output_text)
        task_type = payload.get("task_type", "text")
        score = enriched["meta"].get("diagnostic_score", 0.5)
        final_route = reroute(dispatch_task(task_type, score)) if score < 0.4 else { "fallback": dispatch_task(task_type, score) }

        enriched["output"] = rewritten
        enriched["meta"]["emotion_tag"] = emotion
        enriched["meta"]["final_task_route"] = final_route.get("fallback")
        return jsonify({ "success": True, "result": enriched })
    except Exception as e:
        return jsonify({ "success": False, "error": str(e) }), 500
