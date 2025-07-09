import json, os

MEMORY_LOG = "memory/logs.json"
FEEDBACK_LOG = "memory/feedback_logs.json"

def merge_feedback_into_memory():
    if not os.path.exists(FEEDBACK_LOG): return []

    with open(FEEDBACK_LOG, "r") as f:
        feedbacks = json.load(f)

    with open(MEMORY_LOG, "r") as f:
        memory = json.load(f)

    for fb in feedbacks:
        related = [m for m in memory if fb["input"].strip().lower() == m.get("input", "").strip().lower()]
        for m in related:
            m.setdefault("feedback_reinforcement", []).append(fb["feedback"])
            m["meta"]["reflection_weight"] = m.get("meta", {}).get("reflection_weight", 0.0) + 0.2

    with open(MEMORY_LOG, "w") as f:
        json.dump(memory, f, indent=2)

    return related
