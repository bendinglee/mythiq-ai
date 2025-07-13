from flask import Blueprint, request, jsonify
from branches.plugin_constructor.plugin_builder import build_plugin_code
from branches.plugin_constructor.plugin_writer import write_plugin_file
from branches.plugin_constructor.plugin_exporter import export_plugin_bundle

plugin_constructor_api = Blueprint("plugin_constructor", __name__)

@plugin_constructor_api.route("/api/plugin-construct", methods=["POST"])
def plugin_construct():
    try:
        data = request.get_json()
        code = build_plugin_code(data)
        file_path = write_plugin_file(data["name"], code)
        bundle = export_plugin_bundle(data["name"], code)
        return jsonify({ "success": True, "path": file_path, "export": bundle })
    except Exception as e:
        return jsonify({ "success": False, "error": str(e) })
