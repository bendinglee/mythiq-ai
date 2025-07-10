from flask import Blueprint, request, jsonify
from branches.math_solver.router import solve_math_route
from branches.semantic_search.query_router import semantic_query_route
from branches.memory_core.routes import store_memory
from branches.self_learning.routes import reflect, update
from branches.qa_validator.routes import grade_answer
from branches.seo_master.routes import optimize_keywords_route

core_router_api = Blueprint("core_router", __name__)

@core_router_api.route("/dispatch", methods=["POST"])
def dispatch():
    data = request.get_json()
    intent = data.get("intent")

    if intent == "solve_math":
        return solve_math_route()
    elif intent == "semantic_search":
        return semantic_query_route()
    elif intent == "log_memory":
        return store_memory()
    elif intent == "reflect":
        return reflect()
    elif intent == "update_learning":
        return update()
    elif intent == "qa_grade":
        return grade_answer()
    elif intent == "seo_optimize":
        return optimize_keywords_route()
    else:
        return jsonify({ "success": False, "error": f"Unknown intent: {intent}" }), 400
