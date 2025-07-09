from flask import Flask, request, jsonify, render_template
import os
import traceback
import json
from dotenv import load_dotenv

# 🔐 Load environment variables
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID")

print("🚀 Mythiq startup initiated...")
print("HF_TOKEN present:", bool(HF_TOKEN))
print("WOLFRAM_APP_ID present:", bool(WOLFRAM_APP_ID))

# ✅ Initialize Flask app
app = Flask(__name__, static_url_path='/static')

# 🔁 Fallback-safe dynamic injection
print("🔁 Importing fallback-safe modules...")
try:
    from branches import init_modules
    init_modules(app)
except Exception as e:
    print("❌ Error loading dynamic modules:", traceback.format_exc())

# ✅ Static route imports
try:
    from branches.math_solver.solver import solve_math_query
    from branches.doc_ingestor.routes import load_docs_route
    from branches.general_knowledge.query import answer_general_knowledge
    from branches.intent_router.classifier import classify_intent
    from branches.semantic_search.query_router import query_fuzzy_route
    from branches.self_learning.log import log_entry
    from branches.self_learning.recall import retrieve_entries
    from branches.self_learning.reflect import reflect_summary
    from branches.core_router.dispatcher import dispatch_input
    from branches.image_generator.routes import generate_image_route
    from branches.qa_validator.routes import validate_answer_route
    from branches.seo_master.routes import optimize_keywords_route
    from branches.self_learning.reflection_trainer.trainer_route import reflect_logs_route
    from branches.image_synth.routes import image_api
    from branches.visual_gallery.routes import gallery_api
    app.register_blueprint(image_api)
    app.register_blueprint(gallery_api)
    print("✅ Core route modules loaded.")
except Exception as e:
    print("❌ Core import failed:", traceback.format_exc())

# ✅ API ROUTES

@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({"status": "ok", "message": "Mythiq backend running ✅"})

@app.route("/api/solve-math", methods=["POST"])
def solve_math():
    data = request.get_json()
    try:
        result = solve_math_query(data.get("question", ""))
        return jsonify({"success": True, "result": result})
    except Exception as e:
        print("❌ Math route error:", traceback.format_exc())
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

@app.route("/")
def index():
    return render_template("index.html")

# ✅ Boot confirmation
print("✅ Reached end of main.py — launching Flask...")

if __name__ == "__main__":
    print("🟢 Flask app running at http://localhost:5000")
    app.run(host="0.0.0.0", port=5000)
