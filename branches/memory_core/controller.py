from flask import request, jsonify
import json, os, uuid, datetime

MEMORY_DB = "memory/logs.json"

def load_logs():
    if not os.path.exists(MEMORY_DB): return []
    with open(MEMORY_DB, "r", encoding="utf-8") as f:
        return json.load(f)

def save_logs(logs):
    with open(MEMORY_DB, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)

def log_memory_entry():
    try:
        data = request.get_json()
        logs = load_logs()

        new_entry = {
            "id": str(uuid.uuid4()),
            "input": data.get("input", ""),
            "output": data.get("output", ""),
            "tags": data.get("tags", []),
            "success": data.get("success", False),
            "meta": {
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                "source": data.get("meta", {}).get("source", "unknown"),
                "cleaned_input": data.get("meta", {}).get("cleaned_input", ""),
                "score": data.get("meta", {}).get("score", 0.0),
                "reflection_weight": data.get("meta", {}).get("reflection_weight", 0.0),
                "related_ids": data.get("meta", {}).get("related_ids", [])
            }
        }

        logs.append(new_entry)
        save_logs(logs)

        return jsonify({ "success": True, "id": new_entry["id"] })
    except Exception as e:
        return jsonify({ "success": False, "error": str(e) }), 500

def query_memory():
    try:
        query = request.args.get("q", "").lower()
        logs = load_logs()
        filtered = [log for log in logs if query in log["input"].lower() or query in log["output"].lower()]
        return jsonify({ "success": True, "results": filtered[-10:] })
    except Exception as e:
        return jsonify({ "success": False, "error": str(e) }), 500
