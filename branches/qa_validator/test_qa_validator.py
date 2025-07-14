import requests
import json

BASE_URL = "http://localhost:5000/api"  # Update if hosted elsewhere

# 🌐 Test /qa-grade
def test_qa_grade():
    print("▶ Testing /qa-grade")
    payload = {
        "input": "What is the capital of France?",
        "output": "Paris"
    }
    r = requests.post(f"{BASE_URL}/qa-grade", json=payload)
    print("✅ Response:", r.json())

# 🌐 Test /validate-answer
def test_validate_answer():
    print("▶ Testing /validate-answer")
    payload = {
        "input": "Who wrote Hamlet?",
        "output": "Shakespeare"
    }
    r = requests.post(f"{BASE_URL}/validate-answer", json=payload)
    print("✅ Response:", r.json())

# 🌐 Test /grade-feedback
def test_grade_feedback():
    print("▶ Testing /grade-feedback")
    payload = {
        "input": "Solve: 2 + 2",
        "output": "The answer is 4",
        "meta": {
            "confidence": 0.91,
            "source": "math_solver"
        }
    }
    r = requests.post(f"{BASE_URL}/grade-feedback", json=payload)
    print("✅ Enriched Response:", json.dumps(r.json(), indent=2))

# 🌐 Test /status
def test_status():
    print("▶ Testing /status")
    r = requests.get(f"{BASE_URL}/status")
    print("✅ Healthcheck:", r.json())

# 🚀 Run all
if __name__ == "__main__":
    test_status()
    test_qa_grade()
    test_validate_answer()
    test_grade_feedback()
