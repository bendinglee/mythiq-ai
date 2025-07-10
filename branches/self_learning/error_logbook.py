error_log = []

def log_error(intent, error_msg):
    error_log.append({
        "intent": intent,
        "error": error_msg
    })

def get_error_history():
    return error_log[-10:]
