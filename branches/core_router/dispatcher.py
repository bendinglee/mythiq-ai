from flask import request, jsonify
from branches.intent_router.utils import classify_intent_internal
from branches.feedback_reactor.controller import update_with_feedback
from branches.uncertainty_detector.analyzer import assess_uncertainty
from branches.core_router.fallbacks import fallback_router
from branches.core_router.route_map import route_to_module  # Assumes modular routes

def dispatch_input(request):
    data = request.get_json()
    query = data.get("question", "").strip()

    if not query:
        return jsonify({ "success": False, "error": "No input received." }), 400

    # 🧭 Step 1: Classify intent
    intent = classify_intent_internal(query)
    print(f"[DISPATCH] Intent classified as: {intent}")

    # 🔁 Step 2: Route to module
    try:
        response = route_to_module(intent, query)
    except Exception as e:
        print(f"[ERROR] Routing to module '{intent}' failed:", e)
        return jsonify({ "success": False, "error": str(e) }), 500

    # 🧠 Step 3: Assess uncertainty
    confidence_result = assess_uncertainty(response)
    print(f"[CONFIDENCE] Score: {confidence_result['confidence_score']} | Uncertain: {confidence_result['is_uncertain']}")

    # 🔄 Step 4: Fallback if response is uncertain
    if confidence_result["is_uncertain"]:
        print("[DISPATCH] Low confidence detected — enabling fallback")
        fallback_response = fallback_router(query)

        # 📝 Log feedback for learning
        update_with_feedback({
            "input": query,
            "output": response.get("output", ""),
            "user_feedback": "Uncertain response detected",
            "tags": [intent],
            "confidence": confidence_result["confidence_score"]
        })

        return fallback_response

    # ✅ Step 5: Return confident response
    return response
