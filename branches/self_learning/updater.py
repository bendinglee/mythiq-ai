import json, os, uuid, datetime

MEMORY_LOG = "memory/logs.json"
FEEDBACK_LOG = "memory/feedback_logs.json"
MAX_REFLECTION_WEIGHT = 1.0  # Cap to avoid runaway scoring

def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def merge_feedback_into_memory():
    feedbacks = load_json(FEEDBACK_LOG)
    memory = load_json(MEMORY_LOG)
    updated_entries = []

    for fb in feedbacks:
        fb_input = fb.get("input", "").strip().lower()
        fb_text = fb.get("feedback", "")
        fb_id = fb.get("id", str(uuid.uuid4()))

        if not fb_input or not fb_text:
            continue  # Skip incomplete feedback

        related = [
            m for m in memory
            if fb_input == m.get("input", "").strip().lower()
        ]

        for entry in related:
            meta = entry.setdefault("meta", {})
            history = entry.setdefault("feedback_reinforcement", [])

            if fb_text not in history:
                history.append(fb_text)

            current_weight = meta.get("reflection_weight", 0.0)
            meta["reflection_weight"] = round(min(MAX_REFLECTION_WEIGHT, current_weight + 0.2), 2)

            meta.setdefault("feedback_ids", []).append(fb_id)
            meta["last_feedback"] = datetime.datetime.utcnow().isoformat() + "Z"
            updated_entries.append(entry)

    if updated_entries:
        save_json(MEMORY_LOG, memory)

    return {
        "success": True,
        "updated_count": len(updated_entries
