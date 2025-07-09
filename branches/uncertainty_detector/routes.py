from flask import Blueprint, request, jsonify
from .analyzer import assess_uncertainty

uncertainty_api = Blueprint("uncertainty_detector", __name__)

@uncertainty_api.route("/api/uncertainty", methods=["POST"])
def check_uncertainty():
    data = request.get_json()
    result = assess_uncertainty(data)
    return jsonify(result)
