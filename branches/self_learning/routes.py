from flask import Blueprint, request, jsonify
from branches.self_learning.reflect import generate_reflection
from branches.self_learning.updater import apply_updates
from branches.self_learning.recall import retrieve_memory

self_learning_api = Blueprint("self_learning", __name__)

@self_learning_api.route("/api/self-learn/reflect", methods=["POST"])
def reflect():
    data = request.get_json()
    result = generate_reflection(data)
    return jsonify(result)

@self_learning_api.route("/api/self-learn/update", methods=["POST"])
def update():
    data = request.get_json()
    result = apply_updates(data)
    return jsonify(result)

@self_learning_api.route("/api/self-learn/recall", methods=["GET"])
def recall():
    query = request.args.get("q", "")
    result = retrieve_memory(query)
    return jsonify(result)
