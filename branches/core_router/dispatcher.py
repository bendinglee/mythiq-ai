from branches.feedback_reactor.controller import update_with_feedback
from branches.uncertainty_detector.analyzer import assess_uncertainty

def dispatch_input(request):
    data = request.get_json()
    query = data.get("question", "")

    intent = detect_intent(query)
    response = route_to_module(intent, query)

    # Assess confidence
    confidence_result = assess_uncertainty(response)

    if confidence_result["is_uncertain"]:
        print("[DISPATCH] Low confidence detected — enabling fallback")
        # Trigger fallback module (e.g., general_knowledge or reflect route)
        fallback_response = fallback_router(query)
        # Log feedback entry for long-term memory
        update_with_feedback({
            "input": query,
            "output": response.get("output", ""),
            "user_feedback": "Uncertain response detected",
            "tags": [intent],
            "confidence": confidence_result["confidence_score"]
        })
        return fallback_response
    else:
        return response
