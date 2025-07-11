import requests, traceback, xml.etree.ElementTree as ET, os
from branches.self_learning.log import log_entry

WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID")
WOLFRAM_API = "https://api.wolframalpha.com/v2/query"

def solve_math_query(raw_input):
    original = raw_input.strip()
    cleaned = original.lower().replace("^", "**").replace(" ", "")
    if "=" in cleaned and "for" not in cleaned:
        cleaned += " for x"

    if not WOLFRAM_APP_ID:
        return { "success": False, "error": "Wolfram App ID missing." }

    try:
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
        print("[XML RAW]", res.text[:300])

        return parse_wolfram_response(res.content, original, cleaned)

    except Exception as e:
        print("[WOLFRAM ERROR]", traceback.format_exc())
        return { "success": False, "error": f"Wolfram API error: {str(e)}" }

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

                if any(t in title for t in ["solution", "result", "answer", "root", "exact result"]):
                    payload = {
                        "input": original,
                        "output": text,
                        "tags": ["math", "wolfram"],
                        "success": True,
                        "meta": {
                            "source": "math_solver",
                            "cleaned_input": cleaned_input,
                            "matched_title": title,
                            "score": 0.9,
                            "reflection_weight": 0.15
                        }
                    }

                    log_entry(payload)  # safe call
                    return { "success": True, "result": text }

                if fallback_text is None:
                    fallback_text = text

        if fallback_text:
            return { "success": True, "result": fallback_text }

        return { "success": False, "error": "❌ No readable solution from Wolfram." }

    except Exception as e:
        print("[PARSE ERROR]", traceback.format_exc())
        return { "success": False, "error": f"Parse failed: {str(e)}" }
