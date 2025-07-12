from flask import Blueprint, jsonify
from branches.tutorial_mode.tutorial_renderer import render_tutorial

tutorial_api = Blueprint("tutorial_mode", __name__)

@tutorial_api.route("/tutorial-mode", methods=["GET"])
def tutorial_mode():
    result = render_tutorial()
    return jsonify(result)
