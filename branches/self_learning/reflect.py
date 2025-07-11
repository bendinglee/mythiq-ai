import json, os
from collections import Counter
from flask import jsonify

MEMORY_FILE = os.path.join(os.path.dirname(__file__), "memory.json")

def generate_reflection(entry):
    """Trigger reflection for a single log entry."""
    try:
        score = entry.get("score", 0.0)
        tags = entry.get("tags", [])
        issues = []

        if score < 0.5:
            issues.append("⚠️ Low score — consider output restructuring.")
        if "uncertain" in tags:
            issues.append("🔍 Uncertainty detected — add clarity.")
        if "feedback" in tags:
            issues.append("🔁 Feedback pattern recognized — retrain module.")

        return {
            "success": True,
            "reflection": issues or ["✅ Entry looks solid."]
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Reflection failed: {str(e)}"
        }

def reflect_summary(request):
    """Summarize memory patterns and scoring history."""
    try:
        if not os.path.exists(MEMORY_FILE):
            return jsonify({ "success": True, "summary": "🧠 No memory logs yet." })

        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            memory = json.load(f)

        if not isinstance(memory, list):
            return jsonify({ "success": False, "error": "Memory file format invalid." })

        total_logs = len(memory)
        recent_logs = memory[-3:][::-1]
        success_logs = [m for m in memory if m.get("success", False)]
        failure_logs = total_logs - len(success_logs)

        all_tags = [tag.lower() for m in memory for tag in m.get("tags", []) if isinstance(tag, str)]
        tag_freq = Counter(all_tags).most_common(5)

        scored = [m.get("meta", {}).get("score", 0.0) for m in memory if "score" in m.get("meta", {})]
        avg_score = round(sum(scored) / len(scored), 2) if scored else 0.0

        patterns = []
        if failure_logs > 0:
            patterns.append("⚠️ Failure rate present — refine input validation.")
        if avg_score < 0.5 and scored:
            patterns.append("📉 Average score is low — adjust response depth or clarity.")
        if "feedback" in all_tags:
            patterns.append("🔁 Frequent feedback suggests training improvements underway.")

        summary = {
            "total_logs": total_logs,
            "successful": len(success_logs),
            "failed": failure_logs,
            "top_tags": tag_freq,
            "average_score": avg_score,
            "recent_entries": recent_logs,
            "reflection_patterns": patterns or ["✅ No major issues detected."]
        }

        return jsonify({ "success": True, "summary": summary })

    except Exception as e:
        return jsonify({ "success": False, "error": f"Reflection summary failed: {str(e)}" })
