import requests

def call_route(base_url, route, payload):
    """Send POST request and safely return JSON or error fallback."""
    url = base_url.rstrip("/") + route
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        return { "error": "⏱️ Request timed out." }
    except requests.exceptions.HTTPError as e:
        return { "error": f"❌ HTTP error: {e.response.status_code}" }
    except Exception as e:
        return { "error": f"🚨 Unexpected error: {str(e)}" }

def validate_response(test, response):
    """Run the test’s check function on a response and log failures."""
    try:
        if not isinstance(response, dict):
            return False
        return test["check"](response)
    except Exception as e:
        print(f"[Test Utility] Validation error in '{test.get('name', 'Unnamed')}': {str(e)}")
        return False
