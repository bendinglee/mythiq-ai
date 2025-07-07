import json
import os
from flask import jsonify

MEMORY_FILE = os.path.join(os.path.dirname(__file__), "memory.json")

def retrieve_entries(request):
    tag = request.args.get("tag")
    limit = int(request.args.get("limit", 10))

    try:
        if not os.path.exists(MEMORY_FILE):
            return jsonify({"success": True, "results": []})

        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            memory = json.load(f)

        filtered = memory[::-1]  # reverse for recency

        if tag:
            tag = tag.lower()
            filtered = [m for m in filtered if tag in [t.lower() for t in m.get("tags", [])]]

        return jsonify({
            "success": True,
            "count": len(filtered[:limit]),
            "results": filtered[:limit]
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
