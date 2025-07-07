from flask import Flask, request, jsonify
import os
import wolframalpha

app = Flask(__name__)

# Load Wolfram Alpha App ID from Railway environment variable
WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID")
client = wolframalpha.Client(WOLFRAM_APP_ID)

# ------------------------
# ✅ API Routes
# ------------------------

@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "status": "ok",
        "message": "Mythiq is alive and operational 🧠"
    }), 200

@app.route("/api/solve-math", methods=["POST"])
def solve_math():
    data = request.get_json()
    question = data.get("question", "")
    try:
        res = client.query(question)
        answer = next(res.results).text
        return jsonify({"success": True, "result": answer})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# ------------------------
# 🧠 Frontend
# ------------------------

@app.route("/")
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Mythiq AI</title>
        <style>
            body {
                background-color: #0f0f0f;
                font-family: 'Segoe UI', sans-serif;
                color: #ffffff;
                padding: 40px;
            }
            #chat {
                max-width: 720px;
                margin: auto;
                background: #1f1f1f;
                padding: 20px;
                border-radius: 10px;
            }
            .message {
                margin: 10px 0;
            }
            .user {
                color: #72e0ae;
                font-weight: bold;
            }
            .bot {
                color: #6ab0ff;
            }
        </style>
    </head>
    <body>
        <div id="chat">
            <h2>🤖 Welcome to Mythiq AI</h2>
            <div id="messages"></div>
            <input type="text" id="userInput" placeholder="Type a math question like 'solve x^2 + 5x + 6 = 0'" style="width: 80%;" />
            <button onclick="handleUserMessage()">Send</button>
        </div>

        <script>
            function isMathQuery(message) {
                const mathKeywords = ['solve', 'calculate', 'compute', 'find', 'equation', 'integral', 'derivative', '+', '-', '*', '/', '=', 'x', 'y', '^'];
                return mathKeywords.some(keyword => message.toLowerCase().includes(keyword));
            }

            async function solveMathProblem(question) {
                try {
                    const res = await fetch("/api/solve-math", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ question: question })
                    });
                    const data = await res.json();
                    return data.success ? `🧮 Solution: ${data.result}` : `❌ Error: ${data.error}`;
                } catch (err) {
                    return "❌ Connection error: Could not reach solver.";
                }
            }

            function displayUser(text) {
                const msg = document.createElement("div");
                msg.className = "message user";
                msg.textContent = "🧑 " + text;
                document.getElementById("messages").appendChild(msg);
            }

            function displayBot(text) {
                const msg = document.createElement("div");
                msg.className = "message bot";
                msg.textContent = "🤖 " + text;
                document.getElementById("messages").appendChild(msg);
                document.getElementById("messages").scrollTop = document.getElementById("messages").scrollHeight;
            }

            async function handleUserMessage() {
                const input = document.getElementById("userInput");
                const message = input.value.trim();
                if (!message) return;

                displayUser(message);
                input.value = "";

                if (isMathQuery(message)) {
                    displayBot("🧮 Solving...");
                    const solution = await solveMathProblem(message);
                    displayBot(solution);
                } else {
                    displayBot("🔧 I currently only solve math questions. Try: 'solve x^2 + 5x + 6 = 0'");
                }
            }
        </script>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
