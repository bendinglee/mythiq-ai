import json, os
from branches.plugin_dispatcher.plugin_loader import load_plugin_from_json

MANIFEST_PATH = os.path.join(os.path.dirname(__file__), "store_manifest.json")

def install_preset(pack_name):
    if not os.path.exists(MANIFEST_PATH):
        return { "success": False, "error": "Manifest missing." }

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    pack = next((p for p in manifest.get("packs", []) if p["name"] == pack_name), None)
    if not pack:
        return { "success": False, "error": f"Pack '{pack_name}' not found." }

    installed = []
    for plugin in pack.get("plugins", []):
        result = load_plugin_from_json(plugin["name"], plugin["code"])
        installed.append({ "name": plugin["name"], "status": result.get("success") })

    return { "success": True, "installed": installed }
