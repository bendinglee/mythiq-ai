from flask import Flask, request, jsonify
import os
import requests
import traceback
from xml.etree import ElementTree as ET
from dotenv import load_dotenv
load_dotenv()

# Mythiq Modules
from branches.self_learning.log import log_entry
from branches.self_learning.recall import retrieve_entries
from branches.self_learning.reflect import reflect_summary
from branches.general_knowledge.query import answer_general_knowledge
from branches.intent_router.classifier import classify_intent
from branches.math_solver.solver import solve_math_query

app = Flask(__name__)
WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID")

@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({"status": "ok", "message": "Mythiq backend operational 🧠"}), 200

@app.route("/api/solve-math", methods=["POST"])
def solve_math():
    data = request.get_json()
    question = data.get("question", "").strip()
    result = solve_math_query(question)
    return jsonify(result)

@app.route("/api/log", methods=["POST"])
def log():
    return log_entry(request)

@app.route("/api/recall", methods=["GET"])
def recall():
    return retrieve_entries(request)

@app.route("/api/reflect", methods=["GET"])
def reflect():
    return reflect_summary(request)

@app.route("/api/query-knowledge", methods=["GET"])
def query_knowledge():
    return answer_general_knowledge(request)

@app.route("/api/classify-intent", methods=["GET"])
def route_intent():
    return classify_intent(request)

@app.route("/")
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
      <title>Mythiq AI</title>
      <style>
        body { background: #0f0f0f; color: #fff; font-family: sans-serif; padding: 40px; }
        #chat { max-width: 720px; margin: auto; padding: 20px; background: #1a1a1a; border-radius: 10px; }
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
        async function classifyIntent(query) {
          const res = await fetch("/api/classify-intent?q=" + encodeURIComponent(query));
          const data = await res.json();
          return data.intent || "chat";
        }

        async function solveMath(q) {
          const res = await fetch("/api/solve-math", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: q })
          });
          const data = await res.json();
          return data.success ? `🧮 ${data.result}` : `❌ ${data.error}`;
        }

        async function askKnowledge(q) {
          const res = await fetch("/api/query-knowledge?q=" + encodeURIComponent(q));
          const data = await res.json();
          return data.success ? `📚 ${data.answer}` : `🤖 ${data.answer}`;
        }

        function display(role, text) {
          const box = document.getElementById("messages");
          const msg = document.createElement("div");
          msg.className = "message " + (role === "user" ? "user" : "bot");
          msg.textContent = (role === "user" ? "🧑 " : "🤖 ") + text;
          box.appendChild(msg);
          box.scrollTop = box.scrollHeight;
        }

        async function handleUserMessage() {
          const input = document.getElementById("userInput");
          const text = input.value.trim();
          if (!text) return;
          display("user", text);
          input.value = "";

          const intent = await classifyIntent(text);
          let reply = "";

          if (intent === "math") {
            reply = await solveMath(text);
          } else if (intent === "knowledge") {
            reply = await askKnowledge(text);
          } else {
            reply = "📘 I’m growing smarter every day. Try math or general knowledge queries!";
          }

          display("bot", reply);
        }
      </script>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
