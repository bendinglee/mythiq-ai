from sentence_transformers import SentenceTransformer

def embed_entries(entries):
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    texts = [e["text"] for e in entries]
    embeddings = model.encode(texts, convert_to_tensor=False)
    return [list(vec) for vec in embeddings]
