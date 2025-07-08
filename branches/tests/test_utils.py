import requests

def call_route(base_url, route, payload):
    try:
        res = requests.post(base_url + route, json=payload, timeout=10)
        return res.json()
    except Exception as e:
        return { "error": str(e) }

def validate_response(test, response):
    try:
        return test["check"](response)
    except:
        return False
