from flask import Blueprint, request, jsonify
from branches.feedback_reactor.controller import update_with_feedback
from branches.feedback_reactor.summary_engine import generate_feedback_summary

feedback_api = Blueprint("feedback_reactor", __name__)

@feedback_api.route("/api/feedback-reactor", methods=["POST"])
def react_to_feedback():
    try:
        data = request.get_json()
        result = update_with_feedback(data)

        if result.get("success"):
            return jsonify({
                "success": True,
                "message": "✅ Feedback recorded.",
                "id": result["id"],
                "reflection_score": result.get("reflection_score", 0.0)
            })
        else:
            return jsonify({
                "success": False,
                "error": result.get("error", "Unknown issue while recording feedback.")
            }), 400

    except Exception as e:
        return jsonify({ "success": False, "error": str(e) }), 500

@feedback_api.route("/api/feedback-summary", methods=["GET"])
def feedback_summary_route():
    try:
        summary = generate_feedback_summary()
        return jsonify({
            "success": True,
            "summary": summary
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
