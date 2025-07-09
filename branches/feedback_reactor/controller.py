import json, os, uuid, datetime
from branches.feedback_reactor.validator import validate_feedback
from branches.feedback_reactor.scorer import score_feedback_entry

LOG_PATH = "memory/feedback_logs.json"

def update_with_feedback(data):
    # 🔍 Validate input structure
    if not validate_feedback(data):
        return { "success": False, "error": "Missing required fields: input, output, user_feedback." }

    # 🧠 Score feedback for learning priority
    reflection_score = score_feedback_entry(data)

    # 📦 Build structured entry
    entry = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "input": data["input"],
        "output": data["output"],
        "feedback": data["user_feedback"],
        "tags": data.get("tags", []),
        "confidence": data.get("confidence", 0.5),
        "reflection_score": reflection_score
    }

    # 📝 Ensure log file exists
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w") as f:
            json.dump([], f)

    # 📂 Append to log
    with open(LOG_PATH, "r") as f:
        logs = json.load(f)
    logs.append(entry)

    with open(LOG_PATH, "w") as f:
        json.dump(logs, f, indent=2)

    return { "success": True, "id": entry["id"], "reflection_score": reflection_score }
