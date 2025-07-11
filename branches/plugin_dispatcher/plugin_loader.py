import json, os

REGISTRY_PATH = os.path.join(os.path.dirname(__file__), "plugin_registry.json")

def load_plugin_from_json(name, code):
    if not name or not code:
        return { "success": False, "error": "Missing name or code." }

    plugin = { "name": name, "code": code }

    registry = []
    if os.path.exists(REGISTRY_PATH):
        with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
            registry = json.load(f)

    registry.append(plugin)
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)

    return { "success": True, "message": f"✅ Plugin '{name}' loaded." }
