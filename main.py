from flask import Flask, request, jsonify, render_template
import os, traceback, time, sys
from dotenv import load_dotenv

# 🔐 Environment setup
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID")

print("🚀 Mythiq ignition sequence started.")
print("HF_TOKEN present:", bool(HF_TOKEN))
print("WOLFRAM_APP_ID present:", bool(WOLFRAM_APP_ID))
sys.stdout.flush()

# ✅ Initialize Flask
app = Flask(__name__, static_url_path="/static")

# 🔁 Dynamic module injection
try:
    from branches import init_modules
    init_modules(app)
    print("🔄 Dynamic modules loaded.")
    sys.stdout.flush()
except Exception as e:
    print("❌ Module injection failed:", traceback.format_exc())
    sys.stdout.flush()

# 🔗 Blueprint registration
try:
    # ➕ Import and register all blueprints (same as before)
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
    from branches.image_generator.routes import generate_image_route
    from branches.image_synth.routes import image_api
    from branches.visual_creator.routes import visual_api
    from branches.visual_gallery.routes import gallery_api
    from branches.video_generator.routes import video_api
    from branches.response_formatter.routes import formatter_api
    from branches.user_profile.routes import user_profile_api
    from branches.accessibility_core.routes import accessibility_api
    from branches.task_executor.routes import task_api
    from branches.translation_hub.routes import translation_api
    from branches.api_integrator.routes import api_data_api
    from branches.plugin_dispatcher.routes import plugin_api
    from branches.dataset_tuner.routes import dataset_api
    from branches.templates.routes import templates_api
    from branches.creator_mode.routes import creator_api
    from branches.dashboard_viewer.routes import dashboard_api
    from branches.tutorial_mode.routes import tutorial_api
    from branches.persona_settings.routes import persona_api
    from branches.self_diagnostics.routes import diagnostics_api
    from branches.self_tuner.routes import tuner_api
    from branches.dispatch_optimizer.routes import dispatch_optimizer_api
    from branches.interface_core.routes import interface_api
    from branches.plugin_api_store.routes import plugin_store_api
    from branches.reflex_trainer.response_rewriter import rewrite
    from branches.reflex_trainer.emotion_tagger import tag
    from branches.cortex_fusion.task_dispatcher import dispatch as dispatch_task
    from branches.cortex_fusion.load_balancer import balance
    from branches.cortex_fusion.fallback_router import reroute
    from branches.intent_engine.routes import intent_api
    from branches.memory_core.session_tracker import current_session
    from branches.vector_store.vector_interpreter import interpret_query
    from branches.brain_orchestrator.routes import brain_api

    for bp in [
        image_api, visual_api, gallery_api, video_api,
        formatter_api, user_profile_api, accessibility_api, task_api,
        translation_api, api_data_api, plugin_api, dataset_api, templates_api,
        creator_api, dashboard_api, tutorial_api, persona_api,
        diagnostics_api, tuner_api, dispatch_optimizer_api,
        interface_api, plugin_store_api, intent_api, brain_api
    ]:
        app.register_blueprint(bp)

    print("✅ All branches injected successfully.")
    sys.stdout.flush()
except Exception as e:
    print("❌ Branch registration failed:", traceback.format_exc())
    sys.stdout.flush()

# 🌐 Core API routes
@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "status": "ok",
        "message": "Mythiq backend healthy ✅",
        "timestamp": time.time()
    })

@app.route("/api/solve-math", methods=["POST"])
def solve_math():
    data = request.get_json()
    result = solve_math_query(data.get("question", ""))
    return jsonify({ "success": True, "result": result })

# ➕ Add other @app.route blocks here as needed...

@app.route("/")
def index():
    try:
        return render_template("index.html")
    except Exception as e:
        return jsonify({ "error": "index.html not found", "details": str(e) })

# 🧠 Readiness marker
@app.before_first_request
def on_ready():
    print("✅ Flask app initialized and ready to receive requests.")
    sys.stdout.flush()

# 🚀 Launch Mythiq with diagnostics
if __name__ == "__main__":
    try:
        port = int(os.environ.get("PORT", 5000))
        print(f"🧠 Beginning Flask startup sequence on port {port}...")
        sys.stdout.flush()

        with app.test_request_context():
            registered_routes = [r.rule for r in app.url_map.iter_rules()]
            print("✅ /api/status registered" if "/api/status" in registered_routes else "❌ /api/status NOT found")
            print("🔍 Registered routes:")
            for rule in app.url_map.iter_rules():
                print(f"• {rule.rule} [{', '.join(rule.methods)}]")
            sys.stdout.flush()

        print("📂 Current working directory:", os.getcwd())
        print("📦 Files found:", os.listdir(os.getcwd()))
        sys.stdout.flush()

        app.run(host="0.0.0.0", port=port, debug=False)

    except Exception as e:
        print(f"❌ Flask failed to launch: {e}")
        sys.stdout.flush()
