import os
import faiss
import json
import numpy as np

VEC_DIR = "vector_store"
INDEX_FILE = f"{VEC_DIR}/knowledge_faiss.index"
DATA_FILE = f"{VEC_DIR}/knowledge_index.json"

def save_new_embeddings(entries, embeddings):
    os.makedirs(VEC_DIR, exist_ok=True)

    if os.path.exists(INDEX_FILE):
        index = faiss.read_index(INDEX_FILE)
    else:
        index = faiss.IndexFlatL2(384)

    index.add(np.array(embeddings))

    # Load and append
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            existing = json.load(f)
    else:
        existing = []

    for i, entry in enumerate(entries):
        existing.append({
            "question": entry["question"],
            "answer": entry["answer"],
            "meta": entry.get("meta", {})
        })

    # Write back
    faiss.write_index(index, INDEX_FILE)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2)

    return len(entries)
