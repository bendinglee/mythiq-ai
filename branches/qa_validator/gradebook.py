import os, json
from datetime import datetime

SCORE_FILE = "memory/qa_scores.json"

def log_score(question, answer, score_obj):
    os.makedirs("memory", exist_ok=True)

    entry = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "answer": answer,
        "score": score_obj
    }

    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
    else:
        history = []

    history.append(entry)

    with open(SCORE_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)
