from flask import Blueprint, request, jsonify
from branches.general_knowledge.query import answer_general_knowledge

knowledge_api = Blueprint("general_knowledge", __name__)

@knowledge_api.route("/api/general-knowledge", methods=["POST"])
def general_knowledge_route():
    data = request.get_json()
    query = data.get("q", "")
    response = answer_general_knowledge({ "args": { "q": query } })
    return jsonify(response)
