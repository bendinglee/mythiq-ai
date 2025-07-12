import datetime

tune_log = []

def log_tuning_event(entries):
    tune_log.append({
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "entries": len(entries),
        "tags": [tag for e in entries for tag in e.get("tags", [])]
    })

def get_recent_tuning():
    return tune_log[-5:]
