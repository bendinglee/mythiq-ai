from flask import Blueprint, request, jsonify
from branches.task_executor.reminder_engine import generate_reminder
from branches.task_executor.list_builder import build_checklist
from branches.task_executor.summary_generator import summarize_text

task_api = Blueprint("task_executor", __name__)

@task_api.route("/api/execute-task", methods=["POST"])
def execute_task():
    try:
        data = request.get_json()
        task_type = data.get("task", "")
        content = data.get("content", "")
        style = data.get("style", "default")

        if task_type == "reminder":
            return jsonify(generate_reminder(content))
        elif task_type == "checklist":
            return jsonify(build_checklist(content))
        elif task_type == "summary":
            return jsonify(summarize_text(content, style))
        else:
            return jsonify({ "success": False, "error": "Unknown task type." }), 400

    except Exception as e:
        return jsonify({ "success": False, "error": str(e) }), 500
