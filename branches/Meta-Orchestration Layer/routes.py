from flask import Blueprint, jsonify
from branches.brain_orchestrator.introspector import get_branch_map
from branches.brain_orchestrator.status_renderer import render_brain_status
from branches.brain_orchestrator.reflect_all import trigger_global_reflection

brain_api = Blueprint("brain_orchestrator", __name__)

@brain_api.route("/api/brain-status", methods=["GET"])
def brain_status():
    return jsonify(render_brain_status())

@brain_api.route("/api/branch-map", methods=["GET"])
def branch_map():
    return jsonify(get_branch_map())

@brain_api.route("/api/reflect-all", methods=["POST"])
def reflect_all():
    result = trigger_global_reflection()
    return jsonify(result)
