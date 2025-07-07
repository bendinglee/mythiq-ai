import os, requests, traceback
from xml.etree import ElementTree as ET
from branches.self_learning.log import log_entry
from flask import jsonify, request

WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID")

def solve_math_query(raw_input):
    original = raw_input.strip()
    cleaned = original.lower().replace("^", "**").replace(" ", "")
    if "=" in cleaned and "for" not in cleaned:
        cleaned += " for x"

    try:
        res = requests.get(
            "https://api.wolframalpha.com/v2/query",
            params={
                "input": cleaned,
                "appid": WOLFRAM_APP_ID,
                "format": "plaintext"
            }
        )
        print(f"[WOLFRAM URL] {res.url}")
        print("[WOLFRAM XML RAW]", res.text)

        root = ET.fromstring(res.content)
        for pod in root.findall(".//pod"):
            title = pod.attrib.get("title", "").lower()
            if any(k in title for k in ["solution", "result", "answer", "root", "exact result"]):
                node = pod.find(".//plaintext")
                if node is not None and node.text:
                    result = node.text.strip()

                    # Log result to memory
                    payload = {
                        "input": original,
                        "output": result,
                        "tags": ["math", "wolfram"],
                        "success": True,
                        "meta": {
                            "cleaned_input": cleaned,
                            "source": "math_solver"
                        }
                    }
                    with request.app.test_request_context(json=payload):
                        log_entry(request)

                    return {"success": True, "result": result}

        return {"success": False, "error": "No readable answer from Wolfram Alpha."}

    except Exception as e:
        print("[MATH ERROR]", traceback.format_exc())
        return {"success": False, "error": str(e) or "Unexpected backend error"}
