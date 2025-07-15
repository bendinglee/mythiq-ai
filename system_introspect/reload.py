from flask import Blueprint, jsonify
import importlib
import traceback

reload_api = Blueprint("reload_api", __name__)

MODULE_PATHS = [
    ("branches.status_core.routes", "status_bp"),
    # Add other critical modules if you'd like hot reloads scoped
]

@reload_api.route("/api/reload", methods=["POST"])
def reload_modules():
    reloaded = []
    errors = []
    for path, bp_name in MODULE_PATHS:
        try:
            importlib.reload(importlib.import_module(path))
            reloaded.append(bp_name)
        except Exception as e:
            errors.append({ bp_name: str(e) })
    return jsonify({
        "reloaded": reloaded,
        "errors": errors,
        "status": "complete"
    })
