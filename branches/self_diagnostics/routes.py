from flask import Blueprint, jsonify
from branches.self_diagnostics.test_runner import run_all_tests
from branches.self_diagnostics.score_mapper import compute_score

diagnostics_api = Blueprint("self_diagnostics", __name__)

@diagnostics_api.route("/api/self-test", methods=["GET"])
def self_test():
    results = run_all_tests()
    return jsonify({ "success": True, "results": results })

@diagnostics_api.route("/api/self-health", methods=["GET"])
def self_health():
    results = run_all_tests()
    score = compute_score(results)
    return jsonify({ "success": True, "diagnostic_score": score, "results": results })
