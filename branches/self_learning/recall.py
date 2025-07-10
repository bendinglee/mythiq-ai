import json, os
from flask import jsonify, request
from collections import Counter

MEMORY_FILE = os.path.join(os.path.dirname(__file__), "memory.json")

def retrieve_entries(request):
    try:
        tag = request.args.get("tag", "").lower()
        query = request.args.get("query", "").lower()
        limit = int(request.args.get("limit", 10))

        if not os.path.exists(MEMORY_FILE):
            return jsonify({ "success": True, "results": [], "count": 0 })

        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            memory = json.load(f)

        if not isinstance(memory, list):
            return jsonify({ "success": False, "error": "Memory file format invalid." })

        # Reverse for recency
        filtered = memory[::-1]

        # 🔍 Apply tag filter
        if tag:
            filtered = [
                m for m in filtered
                if any(tag == t.lower() for t in m.get("tags", []))
            ]

        # 🔍 Apply query filter
        if query:
            filtered = [
                m for m in filtered
                if query in m.get("input", "").lower()
                or query in m.get("output", "").lower()
                or any(query in t.lower() for t in m.get("tags", []))
            ]

        # ✨ Slice results to limit
        results = filtered[:limit]

        return jsonify({
            "success": True,
            "count": len(results),
            "results": results,
            "matched_tags": Counter(
                tag for m in results for tag in m.get("tags", []) if isinstance(tag, str)
            ).most_common(3)
        })

    except Exception as e:
        return jsonify({ "success": False, "error": f"Recall failed: {str(e)}" })
