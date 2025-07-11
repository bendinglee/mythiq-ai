import datetime

intent_log = []

def log_intent(user_input, resolved):
    intent_log.append({
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "input": user_input,
        "resolved_intent": resolved["intent"],
        "confidence": resolved["confidence"],
        "source": resolved["source"]
    })

def get_intent_history():
    return intent_log[-10:]
