from flask import Flask, request, jsonify, render_template
import os, traceback
from dotenv import load_dotenv

# 🔐 Environment setup
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID")

print("🚀 Mythiq ignition sequence started.")
print("HF_TOKEN present:", bool(HF_TOKEN))
print("WOLFRAM_APP_ID present:", bool(WOLFRAM_APP_ID))

# ✅ Initialize Flask
app = Flask(__name__, static_url_path="/static")

# 🔁 Dynamic module injection
try:
    from branches import init_modules
    init_modules(app)
    print("🔄 Dynamic modules loaded.")
except Exception as e:
    print("❌ Module injection failed:", traceback.format_exc())

# 🔗 Blueprint registration
try:
    # Core cognition
    from branches.math_solver.solver import solve_math_query
    from branches.general_knowledge.query import answer_general_knowledge
    from branches.semantic_search.query_router import query_fuzzy_route
    from branches.intent_router.classifier import classify_intent
    from branches.core_router.dispatcher import dispatch_input
    from branches.doc_ingestor.routes import load_docs_route
    from branches.qa_validator.routes import validate_answer_route, full_feedback_pipeline
    from branches.self_learning.reflect import reflect_summary
    from branches.self_learning.recall import retrieve_entries
    from branches.self_learning.log import log_entry
    from branches.self_learning.reflection_trainer.trainer_route import reflect_logs_route
    from branches.seo_master.routes import optimize_keywords_route
    from branches.uncertainty_detector.confidence_overlay import confidence_score

    # Generation
    from branches.image_generator.routes import generate_image_route
    from branches.image_synth.routes import image_api
    from branches.visual_creator.routes import visual_api
    from branches.visual_gallery.routes import gallery_api
    from branches.video_generator.routes import video_api
    app.register_blueprint(image_api)
    app.register_blueprint(visual_api)
    app.register_blueprint(gallery_api)
    app.register_blueprint(video_api)

    # Extensions
    from branches.response_formatter.routes import formatter_api
    from branches.user_profile.routes import user_profile_api
    from branches.accessibility_core.routes import accessibility_api
    from branches.task_executor.routes import task_api
    from branches.translation_hub.routes import translation_api
    from branches.api_integrator.routes import api_data_api
    from branches.plugin_dispatcher.routes import plugin_api
    from branches.dataset_tuner.routes import dataset_api

    # Phase 1 additions
    from branches.creator_mode.routes import creator_api
    from branches.dashboard_viewer.routes import dashboard_api
    from branches.tutorial_mode.routes import tutorial_api
    from branches.persona_settings.routes import persona_api
    app.register_blueprint(creator_api)
    app.register_blueprint(dashboard_api)
    app.register_blueprint(tutorial_api)
    app.register_blueprint(persona_api)

    # Phase 2 plugin store
    from branches.plugin_api_store.routes import plugin_store_api
    app.register_blueprint(plugin_store_api)

    # Routing
    from branches.intent_engine.routes import intent_api
    from branches.memory_core.session_tracker import current_session
    from branches.vector_store.vector_interpreter import interpret_query

    # Orchestration
    from branches.brain_orchestrator.routes import brain_api
    app.register_blueprint(formatter_api)
    app.register_blueprint(user_profile_api)
    app.register_blueprint(accessibility_api)
    app.register_blueprint(task_api)
    app.register_blueprint(translation_api)
    app.register_blueprint(api_data_api)
    app.register_blueprint(plugin_api)
    app.register_blueprint(dataset_api)
    app.register_blueprint(intent_api)
    app.register_blueprint(brain_api)

    print("✅ All branches injected successfully.")
except Exception as e:
    print("❌ Branch registration failed:", traceback.format_exc())

# 🌐 API routes

@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({ "status": "ok", "message": "Mythiq backend running ✅" })

@app.route("/api/solve-math", methods=["POST"])
def solve_math():
    data = request.get_json()
    result = solve_math_query(data.get("question", ""))
    return jsonify({ "success": True, "result": result })

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

@app.route("/api/log", methods=["POST"])
def log():
    return log_entry(request)

@app.route("/api/reflect-logs", methods=["POST"])
def reflect_logs():
    return reflect_logs_route()

@app.route("/api/validate-answer", methods=["POST"])
def validate_answer():
    return validate_answer_route()

@app.route("/api/grade-feedback", methods=["POST"])
def grade_feedback():
    return full_feedback_pipeline()

@app.route("/api/optimize-keywords", methods=["POST"])
def optimize_keywords():
    return optimize_keywords_route()

@app.route("/api/classify-intent", methods=["GET"])
def classify():
    return classify_intent(request)

@app.route("/api/dispatch", methods=["POST"])
def dispatch():
    return dispatch_input(request)

@app.route("/api/generate-image", methods=["POST"])
def generate_image():
    return generate_image_route()

@app.route("/api/session", methods=["GET"])
def session():
    return jsonify(current_session())

@app.route("/api/confidence", methods=["POST"])
def confidence():
    return confidence_score(request)

@app.route("/api/interpret-vector", methods=["POST"])
def vector_search():
    return interpret_query(request)

@app.route("/")
def index():
    return render_template("index.html")

print("🎯 Mythiq operational — launching Flask...")

if __name__ == "__main__":
    print("🟢 Running at http://localhost:5000")
    app.run(host="0.0.0.0", port=5000)
