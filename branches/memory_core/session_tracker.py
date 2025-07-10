import uuid, datetime

session_log = []

def log_session(user_input, system_response):
    session_log.append({
        "id": str(uuid.uuid4()),
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "input": user_input,
        "output": system_response
    })

def get_session_history():
    return session_log[-10:]  # recent 10
