from test_config import tests
from test_utils import call_route, validate_response
import json, os
from datetime import datetime

BASE_URL = "http://localhost:5000"
RESULT_PATH = "memory/test_results.json"

def run_all_tests(verbose=True):
    results = []
    passed, failed = 0, 0

    print("🚀 Starting full Mythiq test sweep...\n")

    for test in tests:
        name = test["name"]
        if verbose:
            print(f"🧪 Testing: {name}")
        response = call_route(BASE_URL, test["route"], test["payload"])
        passed_test = validate_response(test, response)

        result = {
            "test": name,
            "passed": passed_test,
            "response": response,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        results.append(result)
        passed += int(passed_test)
        failed += int(not passed_test)

        print("✅ Passed" if passed_test else "❌ Failed")
        if verbose:
            print("-" * 40)

    summary = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "total_tests": len(results),
        "passed": passed,
        "failed": failed,
        "results": results
    }

    try:
        os.makedirs(os.path.dirname(RESULT_PATH), exist_ok=True)
        with open(RESULT_PATH, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
        print(f"\n🧠 Results saved to {RESULT_PATH}")
    except Exception as e:
        print(f"⚠️ Failed to save results: {e}")

    print(f"\n✅ Summary: {passed}/{len(results)} passed — {failed} failed")

if __name__ == "__main__":
    run_all_tests()
