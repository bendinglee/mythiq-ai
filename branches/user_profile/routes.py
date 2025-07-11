from flask import Blueprint, request, jsonify
from branches.user_profile.profile_manager import load_profile, update_profile
from branches.user_profile.profile_validator import validate_profile
from branches.user_profile.preference_engine import get_preferences

user_profile_api = Blueprint("user_profile", __name__)

@user_profile_api.route("/api/user-profile", methods=["GET"])
def get_profile():
    return jsonify(load_profile())

@user_profile_api.route("/api/user-profile", methods=["POST"])
def post_profile():
    data = request.get_json()
    valid, msg = validate_profile(data)
    if not valid:
        return jsonify({ "success": False, "error": msg }), 400

    result = update_profile(data)
    return jsonify(result)

@user_profile_api.route("/api/user-preferences", methods=["GET"])
def get_user_preferences():
    prefs = get_preferences()
    return jsonify({ "success": True, "preferences": prefs })
