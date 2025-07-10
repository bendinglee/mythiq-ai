from flask import Blueprint, request, jsonify
from vector_store.search import query_vector_store

vector_api = Blueprint("vector_store", __name__)

@vector_api.route("/api/vector-search", methods=["POST"])
def vector_search():
    data = request.get_json()
    query = data.get("query", "").strip()
    if not query:
        return jsonify({ "success": False, "error": "Missing query." }), 400

    result = query_vector_store(query)
    return jsonify(result)
