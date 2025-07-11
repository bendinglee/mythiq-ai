from branches.brain_orchestrator.introspector import get_branch_map

def render_brain_status():
    branches = get_branch_map().get("branches", [])
    status = {
        "active": len(branches),
        "total": 19,
        "versions": [b.get("version") for b in branches if "version" in b],
        "names": [b.get("name") for b in branches if "name" in b]
    }
    return {
        "success": True,
        "status": status
    }
