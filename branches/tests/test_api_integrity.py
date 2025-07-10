import requests

def test_dispatch_route():
    try:
        res = requests.post("http://localhost:5000/dispatch", json={ "intent": "solve_math", "question": "2x+5=15" })
        assert res.status_code == 200, "❌ Dispatch failed."
        print("✅ Dispatch route responsive.")
    except Exception as e:
        print(f"❌ API test error: {e}")
