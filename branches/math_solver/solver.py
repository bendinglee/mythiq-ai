import requests
import traceback
import xml.etree.ElementTree as ET
import os
from flask import request
from branches.self_learning.log import log_entry

WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID")
WOLFRAM_API = "https://api.wolframalpha.com/v2/query"

def solve_math_query(raw_input):
    original = raw_input.strip()

    # 🧠 Preprocessing cleanup
    cleaned = original.lower().replace("^", "**").replace(" ", "")
    if "=" in cleaned and "for" not in cleaned:
        cleaned += " for x"

    if not WOLFRAM_APP_ID:
        return { "success": False, "error": "Wolfram Alpha App ID missing." }

    try:
        # 🚀 Send request to Wolfram
        res = requests.get(
            WOLFRAM_API,
            params={
                "input": cleaned,
                "appid": WOLFRAM_APP_ID,
                "format": "plaintext",
                "output": "XML"
            },
            timeout=10
        )

        print(f"[WOLFRAM URL] {res.url}")
        print("[WOLFRAM XML RAW]", res.text[:300])

        return parse_wolfram_response(res.content, original, cleaned)

    except Exception as e:
        print("[MATH ERROR]", traceback.format_exc())
        return {
            "success": False,
            "error": f"❌ Wolfram API failed: {str(e)}"
        }

def parse_wolfram_response(xml_content, original, cleaned_input):
    try:
        root = ET.fromstring(xml_content)
        pods = root.findall(".//pod")

        fallback_text = None

        for pod in pods:
            title = pod.attrib.get("title", "").lower()
            node = pod.find(".//plaintext")

            if node is not None and node.text:
                text = node.text.strip()

                if any(key in title for key in ["solution", "result", "answer", "root", "exact result"]):
                    # ✅ Log and return result
                    payload = {
                        "input": original,
                        "output": text,
                        "tags": ["math", "wolfram"],
                        "success": True,
                        "meta": {
                            "cleaned_input": cleaned_input,
                            "source": "math_solver",
                            "matched_title": title
                        }
                    }

                    try:
                        with request.app.test_request_context(json=payload):
                            log_entry(request)
                    except Exception as log_error:
                        print(f"[Log Failure] {log_error}")

                    return { "success": True, "result": text }

                # 🤖 If no strong match, save fallback
                if fallback_text is None:
                    fallback_text = text

        if fallback_text:
            return { "success": True, "result": fallback_text }

        return { "success": False, "error": "❌ No readable result returned from Wolfram Alpha." }

    except Exception as parse_err:
        print("[MATH PARSE ERROR]", traceback.format_exc())
        return { "success": False, "error": f"Failed to parse Wolfram response: {str(parse_err)}" }
