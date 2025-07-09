import os, json

MODULES_FOLDER = os.path.join(os.path.dirname(__file__), "modules")
_knowledge_cache = {}

def load_all_knowledge():
    global _knowledge_cache
    _knowledge_cache = {}  # Reset on reload

    for file in os.listdir(MODULES_FOLDER):
        if file.endswith(".json"):
            path = os.path.join(MODULES_FOLDER, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    entries = json.load(f)
                    for entry in entries:
                        question = entry.get("question", "").lower()
                        answer = entry.get("answer", "")
                        if question:
                            _knowledge_cache[question] = {
                                "answer": answer,
                                "source": file
                            }
            except Exception as e:
                print(f"⚠️ Failed to load {file}:", e)

    print(f"📘 Loaded {len(_knowledge_cache)} entries from {MODULES_FOLDER}")

def get_knowledge(query):
    if not query or not _knowledge_cache:
        return None

    query = query.lower()
    for known_q, data in _knowledge_cache.items():
        if query in known_q or known_q in query:
            return data["answer"]
    return None
