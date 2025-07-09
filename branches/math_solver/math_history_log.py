import json, os, datetime, uuid

LOG_PATH = "memory/math_history.json"

def log_math_attempt(prompt, result, success=True):
    entry = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "input": prompt,
        "result": result,
        "status": "success" if success else "fail"
    }

    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w") as f:
            json.dump([], f)

    with open(LOG_PATH, "r") as f:
        logs = json.load(f)

    logs.append(entry)

    with open(LOG_PATH, "w") as f:
        json.dump(logs, f, indent=2)
