import faiss
import numpy as np
import json, os

DB_FILE = "vector_store/knowledge_index.json"
EMBED_FILE = "vector_store/knowledge_faiss.index"

def load_knowledge_pairs():
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_vectors(index, embeddings):
    faiss.write_index(index, EMBED_FILE)
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(embeddings, f, indent=2)

def load_index():
    return faiss.read_index(EMBED_FILE)

def search_index(index, query_vec, k=1):
    D, I = index.search(np.array([query_vec]), k)
    return I[0]
