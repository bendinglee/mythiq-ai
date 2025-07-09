import requests
import traceback
import xml.etree.ElementTree as ET
from flask import request
from branches.self_learning.log import log_entry
import os

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
                "format": "plaintext",
                "output": "XML"
            }
        )
        print(f"[WOLFRAM URL] {res.url}")
        print("[WOLFRAM XML RAW]", res.text[:500])  # Truncate for logs

        root = ET.fromstring(res.content)
        pods = root.findall(".//pod")

        fallback_text = None

        for pod in pods:
            title = pod.attrib.get("title", "").lower()
            node = pod.find(".//plaintext")
            if node is not None and node.text:
                text = node.text.strip()
                if any(k in title for k in ["solution", "result", "answer", "root", "exact result"]):
                    result = text

                    # Log and return the result
                    payload = {
                        "input": original,
                        "output": result,
                        "tags": ["math", "wolfram"],
                        "success": True,
                        "meta": {"cleaned_input": cleaned, "source": "math_solver"}
                    }
                    with request.app.test_request_context(json=payload):
                        log_entry(request)

                    return {"success": True, "result": result}
                if fallback_text is None:
                    fallback_text = text

        if fallback_text:
            return {"success": True, "result": fallback_text}

        return {"success": False, "error": "❌ No readable answer returned from Wolfram Alpha."}

    except Exception as e:
        print("[MATH ERROR]", traceback.format_exc())
        return {"success": False, "error": f"Wolfram failed: {str(e)}"}
