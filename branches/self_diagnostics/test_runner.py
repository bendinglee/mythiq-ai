import json, os
import requests

REGISTRY_PATH = os.path.join(os.path.dirname(__file__), "test_registry.json")

def run_all_tests():
    if not os.path.exists(REGISTRY_PATH):
        return []

    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        tests = json.load(f)

    results = []
    for t in tests.get("tests", []):
        endpoint = t.get("endpoint", "")
        input_payload = t.get("input", {})
        expected = t.get("expected", "")

        try:
            res = requests.post(f"http://localhost:5000{endpoint}", json=input_payload, timeout=5)
            output = res.json()
            passed = expected in json.dumps(output)
        except Exception as e:
            output = { "error": str(e) }
            passed = False

        results.append({
            "branch": t.get("branch"),
            "endpoint": endpoint,
            "input": input_payload,
            "expected": expected,
            "output": output,
            "passed": passed
        })

    return results
