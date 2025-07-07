import json
import os
from datetime import datetime
from flask import jsonify

MEMORY_FILE = os.path.join(os.path.dirname(__file__), "memory.json")

def log_entry(request):
    try:
        data = request.get_json()
        log = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "input": data.get("input", ""),
            "output": data.get("output", ""),
            "tags": data.get("tags", []),
            "success": data.get("success", True),
            "meta": data.get("meta", {})
        }

        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                memory = json.load(f)
        else:
            memory = []

        memory.append(log)

        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(memory, f, indent=2)

        return jsonify({"success": True, "message": "Memory logged."})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
