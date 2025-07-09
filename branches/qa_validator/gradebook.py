import json, os, datetime, uuid

GRADE_LOG = "memory/qa_grades.json"

def log_grade(entry, result):
    grade = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "input": entry.get("input"),
        "output": entry.get("output"),
        "score": result.get("score", 0.0),
        "feedback": result.get("feedback", []),
        "tags": result.get("tags", [])
    }

    if not os.path.exists(GRADE_LOG):
        with open(GRADE_LOG, "w") as f: json.dump([], f)

    with open(GRADE_LOG, "r") as f: logs = json.load(f)
    logs.append(grade)

    with open(GRADE_LOG, "w") as f: json.dump(logs, f, indent=2)
