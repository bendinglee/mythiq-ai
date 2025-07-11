from flask import Blueprint, request, jsonify
from branches.plugin_dispatcher.plugin_loader import load_plugin_from_json
from branches.plugin_dispatcher.sandbox_runner import execute_plugin
from branches.plugin_dispatcher.plugin_registry import list_plugins

plugin_api = Blueprint("plugin_dispatcher", __name__)

@plugin_api.route("/api/list-plugins", methods=["GET"])
def get_plugins():
    return jsonify({ "success": True, "plugins": list_plugins() })

@plugin_api.route("/api/load-plugin", methods=["POST"])
def load_plugin():
    try:
        data = request.get_json()
        name = data.get("name", "")
        code = data.get("code", "")
        result = load_plugin_from_json(name, code)
        return jsonify(result)
    except Exception as e:
        return jsonify({ "success": False, "error": str(e) }), 500

@plugin_api.route("/api/run-plugin", methods=["POST"])
def run_plugin():
    try:
        data = request.get_json()
        name = data.get("name", "")
        input_data = data.get("input", "")
        result = execute_plugin(name, input_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({ "success": False, "error": str(e) }), 500
