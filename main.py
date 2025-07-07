from flask import Flask, request, jsonify
import os
import wolframalpha

app = Flask(__name__)

# Load Wolfram API Key
WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID")
client = wolframalpha.Client(WOLFRAM_APP_ID)

# ----------------- BACKEND ENDPOINT -----------------

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

# ----------------- FRONTEND -----------------

@app.route("/")
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Mythiq AI</title>
        <style>
            body { font-family: sans-serif; padding: 20px; background: #0f0f0f; color: #fafafa; }
            #chat { max-width: 700px; margin: auto; padding: 20px; background: #1a1a1a; border-radius: 8px; }
            .message { margin: 10px 0; }
            .user { color: #42b983; }
            .bot  { color: #6db6ff; }
        </style>
    </head>
    <body>
        <div id="chat">
            <h2>🧠 Welcome to Mythiq AI</h2>
            <div id="messages"></div>
            <input type="text" id="userInput" placeholder="Ask something..." style="width: 80%;" />
            <button onclick="handleUserMessage()">Send</button>
        </div>

        <script>
            async function solveMathProblem(question) {
                try {
                    const response = await fetch("/api/solve-math", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ question: question })
                    });
                    const data = await response.json();
                    return data.success
                        ? `🧮 Solution: ${data.result}`
                        : `❌ Error: ${data.error}`;
                } catch (error) {
                    return `❌ Connection Error: ${error.message}`;
                }
            }

            function isMathQuery(message) {
                const mathKeywords = ['solve', 'calculate', 'compute', 'find', 'derivative', 'integral', 'equation', 'factor', 'simplify', 'math', '+', '-', '*', '/', '=', 'x', 'y'];
                return mathKeywords.some(keyword => message.toLowerCase().includes(keyword));
            }

            function displayBotMessage(text) {
                const container = document.getElementById("messages");
                const msg = document.createElement("div");
                msg.className = "message bot";
                msg.textContent = "🤖 " + text;
                container.appendChild(msg);
                container.scrollTop = container.scrollHeight;
            }

            function displayUserMessage(text) {
                const container = document.getElementById("messages");
                const msg = document.createElement("div");
                msg.className = "message user";
                msg.textContent = "🧑 " + text;
                container.appendChild(msg);
            }

            async function handleUserMessage() {
                const input = document.getElementById("userInput");
                const message = input.value.trim();
                if (!message) return;

                displayUserMessage(message);
                input.value = "";

                if (isMathQuery(message)) {
                    displayBotMessage("🧮 Solving...");
                    const response = await solveMathProblem(message);
                    displayBotMessage(response);
                } else {
                    displayBotMessage("🤔 I can only solve math right now. Try something like 'solve 2x + 5 = 15'");
                }
            }
        </script>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

