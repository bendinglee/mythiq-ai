from branches.brain_orchestrator.introspector import get_branch_map
from branches.brain_orchestrator.reflect_all import trigger_global_reflection

def test_orchestrator():
    result = get_branch_map()
    assert result["success"], "❌ Failed to gather branch map."

    reflection = trigger_global_reflection()
    assert reflection["success"], "❌ Global reflection failed."

    print("✅ Brain orchestrator test passed.")

if __name__ == "__main__":
    test_orchestrator()
