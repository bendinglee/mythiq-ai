import json, os, uuid
from sentence_transformers import SentenceTransformer
from branches.semantic_search.embedder import embed_texts
from branches.self_learning.reflection_trainer.vector_updater import save_new_embeddings

LOG_DB = "memory/logs.json"

def extract_failed_queries():
    if not os.path.exists(LOG_DB):
        return []

    try:
        with open(LOG_DB, "r", encoding="utf-8") as f:
            logs = json.load(f)
    except Exception as e:
        print(f"[Trainer] Failed to load logs: {e}")
        return []

    failed = []
    for log in logs:
        if not log.get("success") and isinstance(log.get("input"), str):
            input_text = log["input"].strip()
            if input_text:
                failed.append({
                    "id": str(uuid.uuid4()),
                    "question": input_text,
                    "source": "reflection_log",
                    "meta": log.get("meta", {})
                })
    return failed

def suggest_reflections(failed_entries):
    reflections = []
    seen = set()

    for entry in failed_entries:
        q = entry["question"]
        if q.lower() in seen:
            continue
        seen.add(q.lower())

        guess = f"I'm sorry, I don't have a direct answer. But here's what I know about: {q}"
        reflections.append({
            "id": entry["id"],
            "question": q,
            "answer": guess,
            "meta": entry.get("meta", {}),
            "source": entry.get("source", "trainer")
        })

    return reflections

def reflect_and_embed():
    failed = extract_failed_queries()
    if not failed:
        return {
            "success": False,
            "message": "📭 No failed logs to reflect on."
        }

    reflections = suggest_reflections(failed)
    questions = [r["question"] for r in reflections]

    try:
        # 🧠 Lazy model load
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        embeddings = embed_texts(questions, model=model)
    except Exception as e:
        return {
            "success": False,
            "error": f"Embedding failed: {str(e)}",
            "message": "❌ Reflection embedding interrupted."
        }

    updated = save_new_embeddings(reflections, embeddings)

    return {
        "success": True,
        "updated_count": len(updated),
        "message": "💡 Reflections embedded and stored successfully.",
        "updated_ids": [r["id"] for r in updated]
    }
