from flask import request, jsonify
from branches.self_learning.reflection_trainer.trainer import reflect_and_embed
from branches.self_learning.log import log_entry

def reflect_logs_route():
    result = reflect_and_embed()

    # Optional: log back to memory
    payload = {
        "input": "[Reflection Trainer]",
        "output": result.get("message"),
        "tags": ["self-improve", "reflection"],
        "success": result.get("success", False),
        "meta": { "updated": result.get("updated", 0) }
    }
    with request.app.test_request_context(json=payload):
        log_entry(request)

    return jsonify(result)
