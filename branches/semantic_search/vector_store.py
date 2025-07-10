import faiss
import numpy as np
import json, os

DB_FILE = "vector_store/knowledge_index.json"
EMBED_FILE = "vector_store/knowledge_faiss.index"

def load_knowledge_pairs():
    """Load vector metadata (text + ID mapping)."""
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_vectors(index, metadata_list):
    """Save FAISS index and text→vector metadata."""
    faiss.write_index(index, EMBED_FILE)
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata_list, f, indent=2)

def load_index():
    """Load FAISS index file."""
    if not os.path.exists(EMBED_FILE):
        raise FileNotFoundError("Vector index missing — build it first.")
    return faiss.read_index(EMBED_FILE)

def search_index(index, query_vec, k=5):
    """Search FAISS index and return matched IDs + scores."""
    if index.ntotal == 0:
        return []

    query = np.array([query_vec]).astype('float32')
    D, I = index.search(query, k)
    results = []
    for score, idx in zip(D[0], I[0]):
        results.append({ "id": int(idx), "score": round(float(score), 4) })
    return results
