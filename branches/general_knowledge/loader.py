import os, json

MODULES_FOLDER = os.path.join(os.path.dirname(__file__), "modules")

def get_knowledge(query):
    if not query:
        return None

    for file in os.listdir(MODULES_FOLDER):
        if file.endswith(".json"):
            path = os.path.join(MODULES_FOLDER, file)
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            for entry in data:
                q = entry.get("question", "").lower()
                if query in q or q in query:
                    return entry.get("answer")
    return None
