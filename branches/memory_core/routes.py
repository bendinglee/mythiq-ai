from flask import Blueprint
from branches.memory_core.controller import (
    log_memory_entry,
    query_memory,
    get_memory_stats,
    recall_similar_memory,
    update_memory_feedback
)

memory_api = Blueprint("memory_api", __name__)

@memory_api.route("/memory/log", methods=["POST"])
def log_memory(): return log_memory_entry()

@memory_api.route("/memory/search", methods=["GET"])
def search_memory(): return query_memory()

@memory_api.route("/memory/stats", methods=["GET"])
def stats(): return get_memory_stats()

@memory_api.route("/memory/recall", methods=["POST"])
def recall(): return recall_similar_memory()

@memory_api.route("/memory/feedback", methods=["POST"])
def feedback(): return update_memory_feedback()
