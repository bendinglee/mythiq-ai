from flask import Flask, request, jsonify
import os
import traceback
from dotenv import load_dotenv

# 🔐 Load environment variables
load_dotenv()
WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID")
HF_TOKEN = os.getenv("HF_TOKEN")

app = Flask(__name__)

# ✅ Import critical AI branches
try:
    from branches.self_learning.log import log_entry
    from branches.self_learning.recall import retrieve_entries
    from branches.self_learning.reflect import reflect_summary
    from branches.general_knowledge.query import answer_general_knowledge
    from branches.intent_router.classifier import classify_intent
    from branches.math_solver.solver import solve_math_query
    from branches.semantic_search.query_router import query_fuzzy_route
    from branches.doc_ingestor.routes import load_docs_route
    from branches.core_router.dispatcher import dispatch_input
except Exception as e:
    print("🔥 Core import error:", traceback.format_exc())

# ✅ Optional modules (resilient fallback)
try:
    from branches.self_learning.reflection_trainer.trainer_route import reflect_logs_route
except Exception as e:
    print("🧠 Reflection module unavailable:", e)
    def reflect_logs_route():
        return jsonify({"success": False, "message": "Reflection disabled. Install sentence-transformers."})

try:
    from branches.image_generator.routes import generate_image_route
except Exception as e:
    print("🎨 Image generation module unavailable:", e)
    def generate_image_route():
        return jsonify({"success": False, "message": "Image gen offline. Check HuggingFace or token."})

# ✅ API Endpoints

@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({"status": "ok", "message": "Mythiq backend is alive 🔥"}), 200

@app.route("/api/solve-math", methods=["POST"])
def solve_math():
    try:
        data = request.get_json()
        question = data.get("question", "").strip()
        return jsonify(solve_math_query(question))
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/query-knowledge", methods=["GET"])
def query_knowledge():
    return answer_general_knowledge(request)

@app.route("/api/query-fuzzy", methods=["GET"])
def query_fuzzy():
    return query_fuzzy_route()

@app.route("/api/load-docs", methods=["POST"])
def load_docs():
    return load_docs_route()

@app.route("/api/reflect-logs", methods=["POST"])
def reflect_logs():
    return reflect_logs_route()

@app.route("/api/recall", methods=["GET"])
def recall():
    return retrieve_entries(request)

@app.route("/api/reflect", methods=["GET"])
def reflect():
    return reflect_summary(request)

@app.route("/api/log", methods=["POST"])
def log():
    return log_entry(request)

@app.route("/api/classify-intent", methods=["GET"])
def classify():
    return classify_intent(request)

@app.route("/api/dispatch", methods=["POST"])
def dispatch():
    return dispatch_input(request)

@app.route("/api/generate-image", methods=["POST"])
def generate_image():
    return generate_image_route()

# ✅ Minimal Chat UI
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
        <input type="text" id="userInput" placeholder="Try: generate me a cyberpunk cat" style="width: 75%;" />
        <button onclick="handleUserMessage()">Send</button>
      </div>
      <script>
        async function handleUserMessage() {
          const input = document.getElementById("userInput");
          const text = input.value.trim();
          if (!text) return;
          display("user", text);
          input.value = "";

          const res = await fetch("/api/dispatch", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ input: text })
          });
          const data = await res.json();
          display("bot", data.reply || data.image_url || "🤖 I couldn't generate a response.");
        }

        function display(role, text) {
          const box = document.getElementById("messages");
          const msg = document.createElement("div");
          msg.className = "message " + (role === "user" ? "user" : "bot");
          msg.textContent = (role === "user" ? "🧑 " : "🤖 ") + text;
          box.appendChild(msg);
          box.scrollTop = box.scrollHeight;
        }
      </script>
    </body>
    </html>
    '''

# ✅ Launch app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
