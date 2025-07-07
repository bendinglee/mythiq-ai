from flask import Flask, request, jsonify
import os
import requests
import traceback
from xml.etree import ElementTree as ET

# 🧠 Import memory handlers
from branches.self_learning.log import log_entry
from branches.self_learning.recall import retrieve_entries

app = Flask(__name__)

WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID")

@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "status": "ok",
        "message": "Mythiq backend is operational 🧠"
    }), 200

@app.route("/api/solve-math", methods=["POST"])
def solve_math():
    data = request.get_json()
    question = data.get("question", "").strip()

    if "solve" in question.lower() and "=" in question.lower() and "for" not in question.lower():
        question += " for x"

    try:
        url = "https://api.wolframalpha.com/v2/query"
        params = {
            "input": question,
            "appid": WOLFRAM_APP_ID,
            "format": "plaintext"
        }
        response = requests.get(url, params=params)
        print(f"[WOLFRAM RAW URL] {response.url}")

        root = ET.fromstring(response.content)

        for pod in root.findall(".//pod"):
            title = pod.attrib.get("title", "").lower()
            print(f"[POD] {title}")
            if any(key in title for key in ["result", "solution", "exact result", "answer", "root"]):
                plaintext = pod.find(".//plaintext")
                if plaintext is not None and plaintext.text:
                    result = plaintext.text.strip()

                    # 🔁 Log the successful solve
                    try:
                        from datetime import datetime
                        log_entry_data = {
                            "input": question,
                            "output": result,
                            "tags": ["math", "wolfram"],
                            "success": True,
                            "meta": {"source": "solve-math"}
                        }
                        with app.test_request_context(json=log_entry_data):
                            log_entry(request)
                    except Exception as log_err:
                        print(f"[MEMORY LOGGING ERROR] {log_err}")

                    return jsonify({"success": True, "result": result})

        return jsonify({"success": False, "error": "No solution found in Wolfram Alpha response."})

    except Exception as e:
        print(f"[RAW WOLFRAM EXCEPTION] {repr(e)}")
        print("[TRACEBACK] " + traceback.format_exc())
        return jsonify({
            "success": False,
            "error": str(e) if str(e).strip() else "Unknown backend failure. Check logs for traceback."
        })

# 💾 POST log memory
@app.route("/api/log", methods=["POST"])
def log():
    return log_entry(request)

# 🔍 GET recall memory
@app.route("/api/recall", methods=["GET"])
def recall():
    return retrieve_entries(request)

# 🌐 Frontend UI
@app.route("/")
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Mythiq AI</title>
        <style>
            body { background-color: #0f0f0f; color: #ffffff; font-family: sans-serif; padding: 40px; }
            #chat { max-width: 700px; margin: auto; background: #1c1c1c; padding: 20px; border-radius: 10px; }
            .message { margin: 10px 0; }
            .user { color: #7fffd4; font-weight: bold; }
            .bot { color: #87cefa; }
        </style>
    </head>
    <body>
        <div id="chat">
            <h2>🤖 Welcome to Mythiq AI</h2>
            <div id="messages"></div>
            <input type="text" id="userInput" placeholder="Try: solve 2x + 5 = 15" style="width: 75%;" />
            <button onclick="handleUserMessage()">Send</button>
        </div>

        <script>
            function isMathQuery(msg) {
                const keys = ['solve', 'calculate', 'compute', 'find', '+', '-', '*', '/', '=', '^', 'x', 'y'];
                return keys.some(k => msg.toLowerCase().includes(k));
            }

            async function solveMathProblem(question) {
                try {
                    const res = await fetch("/api/solve-math", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ question })
                    });
                    const data = await res.json();
                    return data.success
                        ? `🧮 Solution: ${data.result}`
                        : `❌ Error: ${data.error || "No readable output from Wolfram."}`;
                } catch (err) {
                    return "❌ Connection error: Could not reach backend.";
                }
            }

            function displayMessage(role, text) {
                const container = document.getElementById("messages");
                const msg = document.createElement("div");
                msg.className = "message " + (role === "user" ? "user" : "bot");
                msg.textContent = (role === "user" ? "🧑 " : "🤖 ") + text;
                container.appendChild(msg);
                container.scrollTop = container.scrollHeight;
            }

            async function handleUserMessage() {
                const input = document.getElementById("userInput");
                const message = input.value.trim();
                if (!message) return;
                displayMessage("user", message);
                input.value = "";

                if (isMathQuery(message)) {
                    displayMessage("bot", "🧮 Solving...");
                    const result = await solveMathProblem(message);
                    displayMessage("bot", result);
                } else {
                    displayMessage("bot", "📘 I currently solve math problems. Try: solve x^2 + 4x + 4 = 0");
                }
            }
        </script>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
