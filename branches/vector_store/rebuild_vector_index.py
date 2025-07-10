import json, os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Paths
META_PATH = "vector_store/knowledge_index.json"
INDEX_PATH = "vector_store/knowledge_faiss.index"

def load_texts():
    if not os.path.exists(META_PATH):
        raise FileNotFoundError("Missing metadata file.")
    with open(META_PATH, "r", encoding="utf-8") as f:
        entries = json.load(f)
    return [entry["text"] for entry in entries]

def embed_texts(texts):
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return model.encode(texts, convert_to_tensor=False)

def build_index(embeddings):
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype('float32'))
    return index

def save_index(index):
    faiss.write_index(index, INDEX_PATH)

def rebuild():
    texts = load_texts()
    embeddings = embed_texts(texts)
    index = build_index(embeddings)
    save_index(index)
    print(f"✅ Rebuilt FAISS index with {len(texts)} entries.")

if __name__ == "__main__":
    rebuild()
