from flask import Blueprint, jsonify
from branches.dashboard_viewer.dashboard_renderer import render_dashboard
from branches.dashboard_viewer.metrics_collector import collect_metrics

dashboard_api = Blueprint("dashboard_viewer", __name__)

@dashboard_api.route("/dashboard", methods=["GET"])
def view_dashboard():
    dashboard = render_dashboard()
    metrics = collect_metrics()
    return jsonify({
        "success": True,
        "dashboard": dashboard,
        "metrics": metrics
    })
