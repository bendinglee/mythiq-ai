import datetime

log = []

def log_access(user_id, action):
    log.append({
        "user": user_id,
        "action": action,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    })

def get_logs():
    return log[-10:]
