from flask import Flask, request, jsonify
import os
import wolframalpha

app = Flask(__name__)

# 🔐 Wolfram Alpha key with fallback parsing enabled
WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID")
client = wolframalpha.Client(WOLFRAM_APP_ID, reinterpret=True)

# ✅ Healthcheck route
@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "status": "ok",
        "message": "Mythiq backend is operational 🧠"
    }), 200

# 🧮 Math solver route with fallback logic + logs
@app.route("/api/solve-math", methods=["POST"])
def solve_math():
    data = request.get_json()
    question = data.get("question", "").strip()

    # Normalize for Wolfram
    if "solve" in question.lower() and "=" in question.lower() and "for" not in question.lower():
        question += " for x"

    try:
        res = client.query(question)
        pod_data = []

        print(f"[WOLFRAM QUERY] {question}")

        for pod in res.pods:
            title = pod.title.lower()
            texts = list(pod.texts)
            pod_data.append((title, texts))
            print(f"[POD] {title} | TEXTS: {texts}")

        if hasattr(res, "results") and res.results:
            text = next(res.results).text
            if text.strip():
                return jsonify({"success": True, "result": text.strip()})

        for title, texts in pod_data:
            if any(key in title for key in ["result", "solution", "solutions", "exact result", "root", "roots", "answer"]):
                for t in texts:
                    if t.strip():
                        return jsonify({"success": True, "result": t.strip()})

        return jsonify({"success": False, "error": "No valid result returned from Wolfram Alpha."})

    except Exception as e:
        print(f"[WOLFRAM EXCEPTION] {repr(e)}")
        return jsonify({"success": False, "error": str(e) or "Unknown error occurred."})

# 🌐 Inline UI
@app.route("/")
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Mythiq AI</title>
        <style>
            body { background-color: #0f0f0f; color: #ffffff; font-family: sans-serif; padding: 40px; }
            #chat { max-width: 720px; margin: auto; background: #1c1c1c; padding: 20px; border-radius: 10px; }
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
                    displayMessage("bot", "📘 I currently support solving math questions only. Try: solve x^2 + 4x + 4 = 0");
                }
            }
        </script>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
