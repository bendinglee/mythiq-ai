from .rules import load_rules

def classify_intent_internal(query):
    query = query.lower()
    try:
        rules = load_rules()
        for label, keywords in rules.items():
            if any(k in query for k in keywords):
                return label
        return "unknown"
    except:
        return "unknown"
