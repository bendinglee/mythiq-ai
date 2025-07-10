import json, os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Paths
META_FILE = "vector_store/knowledge_index.json"
INDEX_FILE = "vector_store/knowledge_faiss.index"

# Load metadata
with open(META_FILE, "r", encoding="utf-8") as f:
    entries = json.load(f)

texts = [entry["text"] for entry in entries]
ids = [entry["id"] for entry in entries]

# Embed
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
embeddings = model.encode(texts, convert_to_tensor=False)

dim = len(embeddings[0])
index = faiss.IndexFlatL2(dim)
index.add(np.array(embeddings).astype('float32'))

# Save index
faiss.write_index(index, INDEX_FILE)
print(f"✅ Rebuilt FAISS index with {len(embeddings)} entries.")
