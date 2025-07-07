from flask import Flask, request, jsonify
import os
import wolframalpha

app = Flask(__name__)

# 🔑 Wolfram Alpha API Key from environment variables
WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID")
client = wolframalpha.Client(WOLFRAM_APP_ID)

# 🔁 Healthcheck route for Railway
@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "status": "ok",
        "message": "Mythiq backend is healthy 🧠"
    }), 200

# 🧮 Math solver route
@app.route("/api/solve-math", methods=["POST"])
def solve_math():
    data = request.get_json()
    question = data.get("question", "")
    try:
        res = client.query(question)
        if hasattr(res, "results") and res.results:
            answer = next(res.results).text
            return jsonify({"success": True, "result": answer})
        else:
            return jsonify({"success": False, "error": "No solution found."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# 🌐 Frontend interface
@app.route("/")
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Mythiq AI</title>
        <style>
            body { background-color: #0f0f0f; color: #ffffff; font-family: sans-serif; padding: 30px; }
            #chat { max-width: 700px; margin: auto; background: #1e1e1e; padding: 20px; border-radius: 8px; }
            .message { margin: 10px 0; }
            .user { color: #7fffd4; font-weight: bold; }
            .bot { color: #87cefa; }
        </style>
    </head>
    <body>
        <div id="chat">
            <h2>🤖 Welcome to Mythiq AI</h2>
            <div id="messages"></div>
            <input type="text" id="userInput" placeholder="Type a math question like 'solve 2x + 5 = 15'" style="width: 75%;" />
            <button onclick="handleUserMessage()">Send</button>
        </div>

        <script>
            function isMathQuery(message) {
                const keywords = ['solve', 'calculate', 'compute', 'find', 'equation', 'simplify', 'integral', 'derivative', '+', '-', '*', '/', '=', 'x', 'y', '^'];
                return keywords.some(keyword => message.toLowerCase().includes(keyword));
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
                        : `❌ Error: ${data.error}`;
                } catch (err) {
                    return "❌ Connection error: Could not reach solver.";
                }
            }

            function displayMessage(className, text) {
                const msg = document.createElement("div");
                msg.className = "message " + className;
                msg.textContent = (className === "user" ? "🧑 " : "🤖 ") + text;
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
                    displayMessage("bot", "🔍 I can only solve math right now. Try something like: solve x^2 + 5x + 6 = 0");
                }
            }
        </script>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
