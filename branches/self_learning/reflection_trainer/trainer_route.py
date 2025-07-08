from flask import request, jsonify, current_app
from branches.self_learning.reflection_trainer.trainer import reflect_and_embed
from branches.self_learning.log import log_entry

def reflect_logs_route():
    try:
        # 🧠 Generate reflection
        result = reflect_and_embed()

        # 📥 Log into memory via simulated request context
        payload = {
            "input": "[Reflection Trainer]",
            "output": result.get("message", ""),
            "tags": ["self-improve", "reflection"],
            "success": result.get("success", False),
            "meta": { "updated": result.get("updated", 0) }
        }

        with current_app.test_request_context('/api/log', method='POST', json=payload):
            log_entry(request)

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Reflection failed: {e}"
        }), 500
