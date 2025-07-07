from flask import Flask, request, jsonify
import os
import wolframalpha

app = Flask(__name__)

# 🔐 Load Wolfram Alpha API key from environment
WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID")
client = wolframalpha.Client(WOLFRAM_APP_ID)

# 🩺 Healthcheck endpoint for Railway
@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "status": "ok",
        "message": "Mythiq backend is healthy 🧠"
    }), 200

# 🧮 Math solver with robust fallback and logging
@app.route("/api/solve-math", methods=["POST"])
def solve_math():
    data = request.get_json()
    question = data.get("question", "").strip()

    if "solve" in question.lower() and "=" in question.lower() and "for" not in question.lower():
        question += " for x"

    try:
        res = client.query(question)

        pod_data = []
        print(f"[WOLFRAM INPUT] {question}")
        for pod in res.pods:
            title = pod.title.lower()
            texts = list(pod.texts)
            pod_data.append((title, texts))
            print(f"[POD] {title} | TEXTS: {texts}")

        if hasattr(res, "results") and res.results:
            text = next(res.results).text
            if text:
                return jsonify({"success": True, "result": text})

        for title, texts in pod_data:
            if any(key in title for key in ["result", "solution", "solutions", "exact result", "root", "answer"]):
                for t in texts:
                    if t.strip():
                        return jsonify({"success": True, "result": t.strip()})

        return jsonify({"success": False, "error": "No valid result returned from Wolfram Alpha."})

    except Exception as e:
        print(f"[WOLFRAM ERROR] {str(e)}")
        return jsonify({"success": False, "error": str(e) or "Unknown error occurred."})

# 💬 Frontend UI (HTML + JS)
@app.route("/")
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Mythiq AI</title>
        <style>
            body { background-color: #0f0f0f; font-family: sans-serif; color: #ffffff; padding: 40px; }
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
            <input type="text" id="userInput" placeholder="Try something like 'solve 2x + 5 = 15'" style="width: 75%;" />
            <button onclick="handleUserMessage()">Send</button>
        </div>

        <script>
            function isMathQuery(message) {
                const keywords = ['solve', 'calculate', 'compute', 'find', 'derivative', 'integral', 'equation', 'simplify', 'factor', '+', '-', '*', '/', '=', 'x', 'y', '^'];
                return keywords.some(kw => message.toLowerCase().includes(kw));
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
                        : `❌ Error: ${data.error || "No readable answer returned."}`;
                } catch (err) {
                    return "❌ Connection error: Could not reach backend.";
                }
            }

            function displayMessage(role, text) {
                const msg = document.createElement("div");
                msg.className = "message " + (role === "user" ? "user" : "bot");
                msg.textContent = (role === "user" ? "🧑 " : "🤖 ") + text;
                document.getElementById("messages").appendChild(msg);
                document.getElementById("messages").scrollTop = document.getElementById("messages").scrollHeight;
            }

            async function handleUserMessage() {
                const input = document.getElementById("userInput");
                const message = input.value.trim();
                if (!message) return;

                displayMessage("user", message);
                input.value = "";

                if (isMathQuery(message)) {
                    displayMessage("bot", "🧮 Solving...");
                    const reply = await solveMathProblem(message);
                    displayMessage("bot", reply);
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
