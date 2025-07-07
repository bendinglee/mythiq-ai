from flask import request, jsonify
from branches.semantic_search.recaller import recall_fuzzy_answer
from branches.self_learning.log import log_entry

def query_fuzzy_route():
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify({"success": False, "error": "Query is required."})

    answer = recall_fuzzy_answer(q)
    if answer:
        log_payload = {
            "input": q,
            "output": answer,
            "tags": ["semantic", "fuzzy"],
            "success": True,
            "meta": {"source": "query-fuzzy"}
        }
        with request.app.test_request_context(json=log_payload):
            log_entry(request)
        return jsonify({"success": True, "answer": answer})

    return jsonify({
        "success": False,
        "answer": "🤖 I couldn’t find a close enough match in memory."
    })
