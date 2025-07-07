from flask import Blueprint, request, jsonify
import os
import wolframalpha

knowledge_api = Blueprint("knowledge_api", __name__)
WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID")
client = wolframalpha.Client(WOLFRAM_APP_ID)

@knowledge_api.route("/api/solve-math", methods=["POST"])
def solve_math():
    data = request.get_json()
    query = data.get("question", "")

    try:
        res = client.query(query)
        answer = next(res.results).text
        return jsonify({"success": True, "result": answer})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


# Export the blueprint
__all__ = ['knowledge_api']
