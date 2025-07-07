from flask import Flask, request, jsonify
import os
import wolframalpha

app = Flask(__name__)

# 🔐 Environment Variable (from Railway Dashboard)
WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID")
client = wolframalpha.Client(WOLFRAM_APP_ID)

# ✅ Healthcheck Route for Railway
@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "status": "ok",
        "message": "Mythiq is running smoothly 🧠"
    }), 200

# 🧮 Math Solver Route with Fallback
@app.route("/api/solve-math", methods=["POST"])
def solve_math():
    data = request.get_json()
    question = data.get("question", "").strip()

    # Normalize input for better Wolfram compatibility
    if "solve" in question.lower() and "=" in question.lower() and "for" not in question.lower():
        question += " for x"

    try:
        res = client.query(question)

        # First try structured result
        if hasattr(res, "results") and res.results:
            answer = next(res.results).text
            return jsonify({"success": True, "result": answer})

        # Fallback through common pod titles
        for pod in res.pods:
            if pod.title.lower() in ["result", "solution", "exact result"]:
                text = next(pod.texts, None)
                if text:
                    return jsonify({"success": True, "result": text})

        return jsonify({"success": False, "error": "No solution returned from Wolfram Alpha."})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# 🖥️ Inline HTML/JS Chat Frontend
@app.route("/")
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Mythiq AI</title>
        <style>
            body { background-color: #0f0f0f; font-family: 'Segoe UI', sans-serif; color: #ffffff; padding: 40px; }
            #chat { max-width: 750px; margin: auto; background: #1e1e1e; padding: 20px; border-radius: 10px; }
            .message { margin: 10px 0; }
            .user { color: #72e0ae; font-weight: bold; }
            .bot { color: #6ab0ff; }
        </style>
    </head>
    <body>
        <div id="chat">
            <h2>🤖 Welcome to Mythiq AI</h2>
            <div id="messages"></div>
            <input type="text" id="userInput" placeholder="Try 'solve 2x + 5 = 15'" style="width: 75%;" />
            <button onclick="handleUserMessage()">Send</button>
        </div>

        <script>
            function isMathQuery(message) {
                const keywords = ['solve', 'calculate', 'compute', 'find', 'integrate', 'derivative', 'equation', 'factor', 'simplify', '+', '-', '*', '/', '=', '^', 'x', 'y'];
                return keywords.some(kw => message.toLowerCase().includes(kw));
            }

            async function solveMathProblem(question) {
                try {
                    const res = await fetch("/api/solve-math", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ question: question })
                    });
                    const data = await res.json();
                    return data.success
                        ? `🧮 Solution: ${data.result}`
                        : `❌ Error: ${data.error}`;
                } catch (err) {
                    return "❌ Connection error: Could not reach math backend.";
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
                    const solution = await solveMathProblem(message);
                    displayMessage("bot", solution);
                } else {
                    displayMessage("bot", "🔍 I currently handle math problems. Try something like: 'solve x^2 + 4x + 4 = 0'");
                }
            }
        </script>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
