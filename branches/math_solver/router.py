from flask import request, jsonify
from branches.math_solver.solver import solve_math_query

def solve_math_route():
    data = request.get_json()
    question = data.get("question", "").strip()
    result = solve_math_query(question)
    return jsonify(result)
