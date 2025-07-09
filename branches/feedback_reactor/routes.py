from flask import Blueprint, request, jsonify
from .controller import update_with_feedback

feedback_api = Blueprint("feedback_reactor", __name__)

@feedback_api.route("/api/feedback-reactor", methods=["POST"])
def react_to_feedback():
    data = request.get_json()
    result = update_with_feedback(data)
    return jsonify(result)
