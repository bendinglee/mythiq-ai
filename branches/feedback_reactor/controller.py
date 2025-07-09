import json, os, uuid, datetime

LOG_PATH = "memory/feedback_logs.json"

def update_with_feedback(data):
    if not data.get("input") or not data.get("output") or not data.get("user_feedback"):
        return { "success": False, "error": "Missing required fields." }

    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w") as f: json.dump([], f)

    with open(LOG_PATH, "r") as f:
        logs = json.load(f)

    entry = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "input": data["input"],
        "output": data["output"],
        "feedback": data["user_feedback"],
        "tags": data.get("tags", []),
        "confidence": data.get("confidence", 0.5)
    }

    logs.append(entry)

    with open(LOG_PATH, "w") as f:
        json.dump(logs, f, indent=2)

    return { "success": True, "id": entry["id"] }
