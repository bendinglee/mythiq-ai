from branches.interface_core.intent_config import runtime_config

def update_intent_config(data):
    if "preset" in data:
        runtime_config["active_preset"] = data["preset"]
    if "tone" in data:
        runtime_config["tone_override"] = data["tone"]
    if "plugin_overrides" in data:
        runtime_config["plugin_overrides"] = data["plugin_overrides"]
    return runtime_config
