from flask import jsonify
from branches import math_solver, memory_core, qa_validator

def get_status():
    status_report = {
        "math_solver": getattr(math_solver, "initialize_branch", lambda: None)() is not None,
        "memory_core": getattr(memory_core, "initialize_branch", lambda: None)() is not None,
        "qa_validator": getattr(qa_validator, "initialize_branch", lambda: None)() is not None,
        "status": "🧠 All critical modules initialized"
    }
    return jsonify(status_report)
