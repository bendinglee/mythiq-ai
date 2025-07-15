from flask import Blueprint, jsonify
import time

bootmap_api = Blueprint("bootmap_api", __name__)

INJECTED_MODULES = [
    "brain_bp", "reflect_bp", "analytics_bp", "intent_bp", "image_bp",
    "persona_bp", "context_bp", "task_bp", "gallery_bp", "dashboard_bp",
    "dialogue_bp", "voice_bp", "agent_bp", "tune_bp", "goal_bp",
    "writer_bp", "search_bp", "bridge_bp", "action_bp", "user_bp",
    "lab_bp", "train_bp", "story_bp", "persona_adapt_bp", "mesh_bp",
    "mobile_bp", "graph_bp", "reflex_bp", "explorer_bp", "secure_bp",
    "lang_bp", "media_bp", "skill_bp", "context_world_bp", "routine_bp",
    "dream_bp", "commerce_bp", "hive_bp", "dialogue_memory_api",
    "ethics_api", "explore_api", "meta_api", "interface_api", "rl_bp",
    "explain_bp", "fed_bp", "imm_bp", "bio_bp"
]

@bootmap_api.route("/api/system/bootmap", methods=["GET"])
def show_bootmap():
    timestamp = time.time()
    return jsonify({
        "inject_map": INJECTED_MODULES,
        "timestamp": timestamp,
        "total": len(INJECTED_MODULES)
    })
