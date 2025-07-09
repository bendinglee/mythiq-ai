import json, os, uuid, datetime

LOG_PATH = "memory/feedback_logs.json"

def write_feedback(entry):
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w") as f: json.dump([], f)

    with open(LOG_PATH, "r") as f:
        logs = json.load(f)

    logs.append({
        "id": str(uuid.uuid4()),
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        **entry
    })

    with open(LOG_PATH, "w") as f:
        json.dump(logs, f, indent=2)
