from .classifier import detect_intent
from .rules import load_route_rules

def route_input(text):
    intent = detect_intent(text)
    rules = load_route_rules()

    route = rules.get(intent, "fallback_core")
    return {
        "intent": intent,
        "route": route,
        "confidence": 0.85 if route != "fallback_core" else 0.3
    }
