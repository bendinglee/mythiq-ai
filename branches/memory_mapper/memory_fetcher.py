import os, json

LOG_PATH = "branches/self_learning/logs/session_log.json"

def fetch_logs():
    if not os.path.exists(LOG_PATH): return []
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("entries", [])
