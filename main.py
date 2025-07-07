from flask import Flask, request, jsonify
import os
import wolframalpha

app = Flask(__name__)

# 🔐 Wolfram Alpha API key from environment
WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID")
client = wolframalpha.Client(WOLFRAM_APP_ID)

# ✅ Railway healthcheck route
@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "status": "ok",
        "message": "Mythiq backend is running 🧠"
    }), 200

# 🧮 Math Solver with input patching + fallback logic + logging
@app.route("/api/solve-math", methods=["POST"])
def solve_math():
    data = request.get_json()
    question = data.get("question", "").strip()

    # Patch input for Wolfram compatibility
    if "solve" in question.lower() and "=" in question.lower() and "for" not in question.lower():
        question += " for x"

    try:
        res = client.query(question)

        # 🚨 Debug: Log pod titles and contents
        print(f"[WOLFRAM INPUT] {question}")
        for pod in res.pods:
            print(f"[POD] {pod.title}")
            for text in pod.texts:
                print(f"  - {text}")

        # First try standard .results
        if hasattr(res, "results") and res.results:
            answer = next(res.results).text
            return jsonify({"success": True, "result": answer})

        # Fallback to broader pod titles
        for pod in res.pods:
            if pod.title.lower() in ["result", "solution", "solutions", "exact result", "root", "roots", "answer"]:
                text = next(pod.texts, None)
                if text:
                    return jsonify({"success": True, "result": text})

        return jsonify({"success": False, "error": "No solution found from Wolfram Alpha."})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# 🌐 Inline HTML frontend
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
            .user { color: #98f5e1; font-weight: bold; }
            .bot { color: #88c0f7; }
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
            function isMathQuery(message) {
                const mathKeywords = ['solve', 'calculate', 'compute', 'find', 'derivative', 'integral', 'simplify', 'equation', 'factor', '+', '-', '*', '/', '=', 'x', 'y', '^'];
                return mathKeywords.some(word => message.toLowerCase().includes(word));
            }

            async function solveMathProblem(question) {
                try {
                    const res = await fetch("/api/solve-math", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ question })
                    });
                    const data = await res.json();
                    return data.success ? `🧮 Solution: ${data.result}` : `❌ Error: ${data.error}`;
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
                    const response = await solveMathProblem(message);
                    displayMessage("bot", response);
                } else {
                    displayMessage("bot", "📘 I currently solve math equations. Try something like: solve x^2 + 4x + 4 = 0");
                }
            }
        </script>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
