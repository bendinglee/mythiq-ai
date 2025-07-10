import requests

tests = [
    {
        "name": "Math Solver",
        "route": "/api/solve-math",
        "payload": { "question": "What is 12*7?" },
        "check": lambda res: "84" in str(res).lower()
    },
    {
        "name": "Image Generator",
        "route": "/api/generate-image",
        "payload": { "prompt": "cyberpunk owl at night", "style": "cinematic" },
        "check": lambda res: "image_url" in res and res["image_url"]
    },
    {
        "name": "SEO Optimizer",
        "route": "/api/optimize-keywords",
        "payload": { "topic": "AI for music composition" },
        "check": lambda res: "title" in res and "ai" in res["title"].lower()
    },
    {
        "name": "Reflection Logs",
        "route": "/api/reflect-logs",
        "payload": {},
        "check": lambda res: "success" in res and res["success"] is True
    }
]

BASE_URL = "http://localhost:5000"  # Change if deployed elsewhere

def run_test_suite():
    print("🚦 Running system integration tests...")
    passed, failed = 0, 0

    for test in tests:
        name = test["name"]
        url = BASE_URL + test["route"]
        try:
            response = requests.post(url, json=test["payload"], timeout=5)
            data = response.json()

            if response.status_code == 200 and test["check"](data):
                print(f"✅ {name} passed.")
                passed += 1
            else:
                print(f"❌ {name} failed.")
                failed += 1
        except Exception as e:
            print(f"❌ {name} error: {str(e)}")
            failed += 1

    print(f"\n🧠 Test Summary: {passed} passed / {failed} failed\n")

if __name__ == "__main__":
    run_test_suite()
