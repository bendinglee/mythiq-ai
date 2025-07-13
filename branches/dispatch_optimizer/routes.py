from flask import Blueprint, request, jsonify
from branches.dispatch_optimizer.adaptive_dispatcher import dynamic_dispatch

dispatch_optimizer_api = Blueprint("dispatch_optimizer", __name__)

@dispatch_optimizer_api.route("/api/dispatch-optimize", methods=["POST"])
def dispatch_optimize():
    try:
        payload = request.get_json()
        result = dynamic_dispatch(payload)
        return jsonify({ "success": True, "routed": result })
    except Exception as e:
        return jsonify({ "success": False, "error": str(e) }), 500
