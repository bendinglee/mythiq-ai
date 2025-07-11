from branches.brain_orchestrator.brain_orchestrator import ACTIVE_BRANCHES

def get_branch_map():
    result = []
    for b in ACTIVE_BRANCHES:
        info = getattr(b, "initialize_branch", lambda: None)()
        if isinstance(info, dict):
            result.append(info)
    return { "success": True, "branches": result }
