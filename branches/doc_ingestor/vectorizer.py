import faiss
import numpy as np
import json
import os

VEC_DIR = "vector_store"
VEC_FILE = f"{VEC_DIR}/knowledge_faiss.index"
DB_FILE = f"{VEC_DIR}/knowledge_index.json"

def load_vector_store():
    if os.path.exists(VEC_FILE):
        index = faiss.read_index(VEC_FILE)
    else:
        index = faiss.IndexFlatL2(384)  # for MiniLM
    return index

def save_vector_store(index, store):
    faiss.write_index(index, VEC_FILE)
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(store, f, indent=2)

def append_chunks(chunks, source="uploaded_doc", embed_fn=None):
    assert embed_fn, "Embed function required"
    os.makedirs(VEC_DIR, exist_ok=True)

    index = load_vector_store()
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            store = json.load(f)
    else:
        store = []

    embeddings = embed_fn(chunks)
    index.add(np.array(embeddings))

    for i, chunk in enumerate(chunks):
        store.append({
            "question": chunk,
            "answer": chunk,
            "meta": {"source": source}
        })

    save_vector_store(index, store)
    return {"success": True, "chunks_added": len(chunks)}
