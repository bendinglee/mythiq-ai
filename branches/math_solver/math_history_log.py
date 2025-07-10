import json, os, uuid, datetime

LOG_FILE = "memory/math_history.json"

def log_math_result(input_text, result_text, success=True):
    entry = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "input": input_text,
        "output": result_text,
        "status": "success" if success else "fail"
    }

    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            logs = json.load(f)

    logs.append(entry)

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)
