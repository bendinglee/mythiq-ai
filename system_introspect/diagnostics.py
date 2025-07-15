from flask import Blueprint, jsonify
import time

diagnostics_api = Blueprint("diagnostics_api", __name__)
BOOT_TIME = time.time()

@diagnostics_api.route("/api/diagnostics/core", methods=["GET"])
def diagnostics():
    return jsonify({
        "boot_time": BOOT_TIME,
        "uptime": round(time.time() - BOOT_TIME, 2),
        "modules_loaded": 50,
        "status_core": "online",
        "reflection_enabled": True,
        "memory_core_active": True
    })
