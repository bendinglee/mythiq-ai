from flask import Blueprint, jsonify
from branches.memory_mapper.grid_builder import build_grid
from branches.memory_mapper.persona_timeline import get_timeline

memory_mapper_api = Blueprint("memory_mapper", __name__)

@memory_mapper_api.route("/api/memory-map", methods=["GET"])
def memory_map():
    grid = build_grid()
    return jsonify({ "success": True, "grid": grid })

@memory_mapper_api.route("/api/persona-timeline", methods=["GET"])
def persona_evolution():
    timeline = get_timeline()
    return jsonify({ "success": True, "timeline": timeline })
