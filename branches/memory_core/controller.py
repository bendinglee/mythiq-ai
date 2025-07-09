import json, os, uuid, datetime
from flask import request, jsonify
from branches.memory_core.scorer import score_memory_entry

MEMORY_DB = "memory/logs.json"

def load_logs():
    if not os.path.exists(MEMORY_DB):
        return []
    with open(MEMORY_DB, "r", encoding="utf-8") as f:
        return json.load(f)

def save_logs(logs):
    with open(MEMORY_DB, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)

def log_memory_entry():
    try:
        data = request.get_json()
        if not data.get("input") or not data.get("output"):
            return jsonify({ "success": False, "error": "Missing 'input' or 'output' fields." }), 400

        logs = load_logs()

        entry = {
            "id": str(uuid.uuid4()),
            "input": data["input"],
            "output": data["output"],
            "tags": data.get("tags", []),
            "success": data.get("success", True),
            "meta": {
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                "source": data.get("meta", {}).get("source", "memory_core"),
                "cleaned_input": data.get("meta", {}).get("cleaned_input", ""),
                "score": data.get("meta", {}).get("score", score_memory_entry(data)),
                "reflection_weight": data.get("meta", {}).get("reflection_weight", 0.0),
                "related_ids": data.get("meta", {}).get("related_ids", [])
            }
        }

        logs.append(entry)
        save_logs(logs)

        return jsonify({ "success": True, "id": entry["id"], "score": entry["meta"]["score"] })

    except Exception as e:
        return jsonify({ "success": False, "error": str(e) }), 500

def query_memory():
    try:
        query = request.args.get("q", "").lower()
        tag_filter = request.args.get("tag", "").lower()
        logs = load_logs()

        results = []
        for log in logs:
            match_input = query in log["input"].lower()
            match_output = query in log["output"].lower()
            match_tags = tag_filter in [t.lower() for t in log.get("tags", [])]

            if query and (match_input or match_output):
                results.append(log)
            elif tag_filter and match_tags:
                results.append(log)

        return jsonify({
            "success": True,
            "results": sorted(results, key=lambda x: x["meta"]["timestamp"], reverse=True)[:10]
        })

    except Exception as e:
        return jsonify({ "success": False, "error": str(e) }), 500
