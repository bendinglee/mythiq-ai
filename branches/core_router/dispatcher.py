from flask import request, jsonify
from branches.intent_router.classifier import classify_intent
from branches.general_knowledge.query import answer_general_knowledge
from branches.math_solver.solver import solve_math_query
from branches.self_learning.log import log_entry

def dispatch_input(req):
    data = req.get_json()
    q = data.get("input", "").strip()

    intent_response = classify_intent_from_text(q)
    intent = intent_response.get("intent", "chat")
    output = ""

    if intent == "math":
        result = solve_math_query(q)
        output = result.get("result") or result.get("error")

    elif intent == "knowledge":
        result = answer_general_knowledge(req)
        data = result.get_json()
        output = data.get("answer") or "No answer found."

    else:
        output = "🤖 I'm still learning. Try math or knowledge queries."

    # Memory log
    log_payload = {
        "input": q,
        "output": output,
        "tags": [intent],
        "success": True,
        "meta": {"source": "dispatch"}
    }
    with req.app.test_request_context(json=log_payload):
        log_entry(req)

    return jsonify({"success": True, "intent": intent, "reply": output})

def classify_intent_from_text(text):
    with request.app.test_request_context(query_string={"q": text}):
        res = classify_intent(request)
        return res.get_json()
