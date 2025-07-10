intent_log = []

def log_intent(intent, result):
    entry = {
        "intent": intent,
        "success": result.get("success", False),
        "timestamp": result.get("timestamp", "")
    }
    intent_log.append(entry)

def get_intent_stats():
    return {
        "total": len(intent_log),
        "success": sum(1 for e in intent_log if e["success"]),
        "failure": sum(1 for e in intent_log if not e["success"])
    }
