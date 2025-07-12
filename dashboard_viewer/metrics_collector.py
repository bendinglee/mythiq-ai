import json, os
from collections import Counter

LOG_PATH = os.path.join(os.path.dirname(__file__), "../self_learning/memory.json")

def collect_metrics():
    if not os.path.exists(LOG_PATH):
        return { "status": "No memory file available." }

    with open(LOG_PATH, "r", encoding="utf-8") as f:
        memory = json.load(f)

    scored = [m.get("meta", {}).get("score", 0.0) for m in memory if "score" in m.get("meta", {})]
    failures = len([m for m in memory if not m.get("success", True)])
    tags = [tag.lower() for m in memory for tag in m.get("tags", []) if isinstance(tag, str)]

    return {
        "total_entries": len(memory),
        "average_score": round(sum(scored)/len(scored), 2) if scored else 0,
        "failure_rate": round(failures / len(memory), 2) if memory else 0,
        "top_tags": Counter(tags).most_common(5)
    }
