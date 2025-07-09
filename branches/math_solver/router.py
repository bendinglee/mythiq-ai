from flask import request, jsonify
from branches.math_solver.solver import solve_math_query

def solve_math_route():
    try:
        data = request.get_json()
        question = data.get("question", "").strip()

        if not question:
            return jsonify({
                "success": False,
                "error": "❌ No math query provided.",
                "input": question
            }), 400

        result = solve_math_query(question)

        if not result.get("success"):
            return jsonify({
                "success": False,
                "error": result.get("error", "Failed to process query."),
                "input": question
            })

        return jsonify({
            "success": True,
            "solution": result.get("result"),
            "confidence": 0.9,
            "tags": ["math_solver"],
            "input": question
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"❌ Internal error: {str(e)}"
        }), 500
