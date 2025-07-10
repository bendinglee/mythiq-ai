import faiss, json, os
import numpy as np

INDEX_PATH = "vector_store/knowledge_faiss.index"
META_PATH = "vector_store/knowledge_index.json"

def load_index():
    if not os.path.exists(INDEX_PATH):
        raise FileNotFoundError("Missing FAISS index.")
    return faiss.read_index(INDEX_PATH)

def save_index(index):
    faiss.write_index(index, INDEX_PATH)

def load_metadata():
    if not os.path.exists(META_PATH):
        return []
    with open(META_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_metadata(data):
    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def search_index(index, query_vec, top_k=5):
    query = np.array([query_vec]).astype('float32')
    D, I = index.search(query, top_k)
    return [{"id": int(i), "score": round(float(d), 4)} for i, d in zip(I[0], D[0])]
