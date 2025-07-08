import json
from sentence_transformers import SentenceTransformer
from branches.semantic_search.embedder import embed_texts
from branches.self_learning.reflection_trainer.vector_updater import save_new_embeddings

LOG_DB = "memory/logs.json"

# 🚀 Load model using built-in SentenceTransformer logic
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def extract_failed_queries():
    try:
        with open(LOG_DB, "r", encoding="utf-8") as f:
            logs = json.load(f)
    except:
        return []

    failed = []
    for log in logs:
        if not log.get("success") and log.get("input"):
            failed.append({
                "question": log["input"],
                "source": "reflection_log",
                "meta": log.get("meta", {})
            })
    return failed

def suggest_reflections(failed_entries):
    reflections = []
    for entry in failed_entries:
        q = entry["question"]
        guess = f"I'm sorry, I don't have a direct answer. But here's what I know about: {q}"
        reflections.append({ "question": q, "answer": guess, "meta": entry.get("meta", {}) })
    return reflections

def reflect_and_embed():
    failed = extract_failed_queries()
    if not failed:
        return { "success": False, "message": "No failed logs to reflect on." }

    reflections = suggest_reflections(failed)
    questions = [r["question"] for r in reflections]
    embeddings = embed_texts(questions)

    updated = save_new_embeddings(reflections, embeddings)
    return {
        "success": True,
        "updated": updated,
        "message": "💡 Reflections embedded and added to memory."
    }
