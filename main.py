from flask import Flask, request, jsonify, render_template
import os
import traceback
import json
from dotenv import load_dotenv

# 🔐 Load environment variables
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID")

app = Flask(__name__, static_url_path='/static')

# ✅ Core AI modules
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
    print("🔥 Core module import error:", traceback.format_exc())

# 🧠 Reflection engine (fallback-safe)
try:
    from branches.self_learning.reflection_trainer.trainer_route import reflect_logs_route
except Exception as e:
    print("🧠 Reflection module unavailable:", e)
    def reflect_logs_route():
        return jsonify({"success": False, "message": "Reflection module not installed."})

# 🎨 Image generator
try:
    from branches.image_generator.routes import generate_image_route
except Exception as e:
    print("🎨 Image generator unavailable:", e)
    def generate_image_route():
        return jsonify({"success": False, "message": "Image generation module offline."})

# 🔎 SEO optimizer
try:
    from branches.seo_master.routes import optimize_keywords_route
except Exception as e:
    print("🔍 SEO module unavailable:", e)
    def optimize_keywords_route():
        return jsonify({"success": False, "message": "SEO module not available."})

# 🧪 QA validator
try:
    from branches.qa_validator.routes import validate_answer_route
except Exception as e:
    print("🧪 QA validator offline:", e)
    def validate_answer_route():
        return jsonify({"success": False, "message": "QA validation module unavailable."})

# ✅ ROUTES

@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({"status": "ok", "message": "Mythiq backend is live 🔥"})

@app.route("/api/solve-math", methods=["POST"])
def solve_math():
    data = request.get_json()
    return jsonify(solve_math_query(data.get("question", "")))

@app.route("/api/query-knowledge", methods=["GET"])
def query_knowledge():
    return answer_general_knowledge(request)

@app.route("/api/query-fuzzy", methods=["GET"])
def query_fuzzy():
    return query_fuzzy_route()

@app.route("/api/load-docs", methods=["POST"])
def load_docs():
    return load_docs_route()

@app.route("/api/recall", methods=["GET"])
def recall():
    return retrieve_entries(request)

@app.route("/api/reflect", methods=["GET"])
def reflect():
    return reflect_summary(request)

@app.route("/api/reflect-logs", methods=["POST"])
def reflect_logs():
    return reflect_logs_route()

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

@app.route("/api/validate-answer", methods=["POST"])
def validate_answer():
    return validate_answer_route()

@app.route("/api/optimize-keywords", methods=["POST"])
def optimize_keywords():
    return optimize_keywords_route()

@app.route("/gallery")
def gallery():
    try:
        with open("memory/image_logs.json", "r", encoding="utf-8") as f:
            logs = json.load(f)
        html = "<h2>🖼️ Mythiq Gallery</h2><div style='display:grid;gap:20px;'>"
        for entry in reversed(logs[-50:]):
            prompt = entry.get("crafted_prompt", entry.get("input_prompt", ""))
            img = entry.get("image_url", "")
            html += f"<div><img src='{img}' style='max-width:100%;border-radius:8px;'/><p>{prompt}</p></div>"
        html += "</div>"
        return html
    except Exception as e:
        return f"<h2>Gallery Load Error:</h2><pre>{e}</pre>"

# ✅ Load web frontend
@app.route("/")
def index():
    return render_template("index.html")

# ✅ Start app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
