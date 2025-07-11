from branches.plugin_dispatcher.sandbox_runner import execute_plugin
from branches.plugin_dispatcher.plugin_loader import load_plugin_from_json

def test_plugin_system():
    plugin = { "name": "math_plus", "code": "def run(x): return int(x)+10" }
    load_plugin_from_json(plugin["name"], plugin["code"])
    result = execute_plugin("math_plus", "7")
    assert result["success"] and result["output"] == 17, "❌ Plugin output mismatch"
    print("✅ Plugin Dispatcher test passed.")

if __name__ == "__main__":
    test_plugin_system()
