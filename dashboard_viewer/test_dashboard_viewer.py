from branches.dashboard_viewer.dashboard_renderer import render_dashboard
from branches.dashboard_viewer.metrics_collector import collect_metrics

def test_dashboard():
    dashboard = render_dashboard()
    metrics = collect_metrics()

    assert "branches" in dashboard, "❌ Branches missing"
    assert "recent_memory" in dashboard, "❌ Memory missing"
    assert "average_score" in metrics, "❌ Metrics incomplete"

    print("✅ Dashboard Viewer test passed.")

if __name__ == "__main__":
    test_dashboard()
