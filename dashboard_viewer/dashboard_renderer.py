from branches.brain_orchestrator.introspector import get_branch_map
from branches.self_learning.recall import retrieve_entries

def render_dashboard():
    branch_data = get_branch_map().get("branches", [])
    memory = retrieve_entries(limit=5).get("entries", [])

    return {
        "branches": branch_data,
        "recent_memory": memory,
        "summary": {
            "total_branches": len(branch_data),
            "recent_entries": len(memory)
        }
    }
