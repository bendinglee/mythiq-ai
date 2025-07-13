from flask import Blueprint, request, jsonify
from branches.plugin_api_store.store_browser import list_store_plugins
from branches.plugin_api_store.preset_installer import install_preset

plugin_store_api = Blueprint("plugin_api_store", __name__)

@plugin_store_api.route("/api/plugin-store", methods=["GET"])
def plugin_store():
    return jsonify({ "success": True, "available": list_store_plugins() })

@plugin_store_api.route("/api/install-preset", methods=["POST"])
def install_plugin_pack():
    data = request.get_json()
    pack_name = data.get("pack", "")
    result = install_preset(pack_name)
    return jsonify(result)
