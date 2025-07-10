import json, os, uuid
from datetime import datetime
from flask import jsonify, request

MEMORY_FILE = os.path.join(os.path.dirname(__file__), "memory.json")

def log_entry(request):
    try:
        data = request.get_json()

        # 🧪 Validate required fields
        input_text = data.get("input", "")
        output_text = data.get("output", "")
        tags = data.get("tags", [])
        success = data.get("success", True)
        meta = data.get("meta", {})

        if not input_text or not output_text:
            return jsonify({
                "success": False,
                "error": "Missing required input or output fields."
            }), 400

        # 🧠 Build memory log
        log = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "input": input_text,
            "output": output_text,
            "tags": tags,
            "success": success,
            "meta": {
                "source": meta.get("source", "self_learning"),
                "score": meta.get("score", 0.0),
                "reflection_weight": meta.get("reflection_weight", 0.0),
                "feedback_ids": meta.get("feedback_ids", []),
                "related_ids": meta.get("related_ids", [])
            }
        }

        # 📦 Load existing memory
        memory = []
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                memory = json.load(f)

        memory.append(log)

        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(memory, f, indent=2)

        return jsonify({
            "success": True,
            "message": "🧠 Memory logged successfully.",
            "id": log["id"],
            "score": log["meta"]["score"]
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Logging failed: {str(e)}"
        }), 500
