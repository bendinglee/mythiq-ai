import json
import os
from collections import Counter
from flask import jsonify

MEMORY_FILE = os.path.join(os.path.dirname(__file__), "memory.json")

def reflect_summary(request):
    try:
        if not os.path.exists(MEMORY_FILE):
            return jsonify({"success": True, "summary": "No memory logs yet."})

        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            memory = json.load(f)

        total = len(memory)
        recent = memory[-3:][::-1]  # most recent 3
        successes = sum(1 for m in memory if m.get("success", False))
        failures = total - successes

        # Tag analysis
        all_tags = [tag.lower() for m in memory for tag in m.get("tags", [])]
        tag_freq = Counter(all_tags).most_common(5)

        summary = {
            "total_logs": total,
            "successful": successes,
            "failed": failures,
            "top_tags": tag_freq,
            "recent": recent
        }

        return jsonify({"success": True, "summary": summary})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
