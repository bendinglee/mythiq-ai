from test_config import tests
from test_utils import call_route, validate_response
import json

BASE_URL = "http://localhost:5000"

def run_all_tests():
    results = []
    for test in tests:
        print(f"🧪 Running: {test['name']}")
        response = call_route(BASE_URL, test["route"], test["payload"])
        passed = validate_response(test, response)
        results.append({
            "test": test["name"],
            "passed": passed,
            "response": response
        })
        print("✅ Passed" if passed else "❌ Failed")
        print("-" * 40)
    
    with open("memory/test_results.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run_all_tests()
