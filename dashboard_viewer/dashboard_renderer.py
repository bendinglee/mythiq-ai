from branches.brain_orchestrator.introspector import get_branch_map
from branches.self_learning.recall import retrieve_entries
from branches.self_diagnostics.test_runner import run_all_tests
from branches.self_diagnostics.score_mapper import compute_score

def render_dashboard():
    branch_data = get_branch_map().get("branches", [])
    memory = retrieve_entries(limit=5).get("entries", [])
    diagnostics = run_all_tests()
    diag_score = compute_score(diagnostics)

    return {
        "branches": branch_data,
        "recent_memory": memory,
        "summary": {
            "total_branches": len(branch_data),
            "recent_entries": len(memory),
            "diagnostic_score": diag_score
        },
        "diagnostics": diagnostics
    }
