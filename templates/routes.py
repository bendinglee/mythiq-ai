from flask import Blueprint, jsonify
from branches.templates.dispatcher import load_templates

templates_api = Blueprint("templates", __name__)

@templates_api.route("/api/templates", methods=["GET"])
def template_list():
    templates = load_templates()
    return jsonify({ "success": True, "templates": templates })
