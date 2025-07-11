def execute_plugin(name, input_data):
    import json, os
    from types import FunctionType

    registry_file = os.path.join(os.path.dirname(__file__), "plugin_registry.json")
    if not os.path.exists(registry_file):
        return { "success": False, "error": "Registry missing." }

    with open(registry_file, "r", encoding="utf-8") as f:
        registry = json.load(f)

    match = next((p for p in registry if p["name"] == name), None)
    if not match:
        return { "success": False, "error": f"Plugin '{name}' not found." }

    try:
        # Secure sandbox execution
        local_env = {}
        exec(match["code"], {}, local_env)
        plugin_fn = local_env.get("run")

        if not isinstance(plugin_fn, FunctionType):
            return { "success": False, "error": "Invalid plugin format." }

        result = plugin_fn(input_data)
        return { "success": True, "output": result }

    except Exception as e:
        return { "success": False, "error": f"Plugin error: {str(e)}" }
