from sentence_transformers import SentenceTransformer
import torch

_embedder = None

def get_embedder():
    """Lazily loads and caches the SentenceTransformer model."""
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return _embedder

def embed_text(text):
    """Embeds a single string and returns a flat tensor list."""
    if not isinstance(text, str):
        text = str(text)
    model = get_embedder()

    try:
        embedding = model.encode([text], convert_to_tensor=True)
        return embedding[0].tolist()  # flatten first tensor
    except Exception as e:
        print(f"[Embedder] Single embedding failed: {e}")
        return []

def embed_texts(texts, model=None):
    """Embeds a list of strings into vector tensors."""
    if not model:
        model = get_embedder()

    cleaned_texts = [str(t).strip() for t in texts if isinstance(t, str) and t.strip()]
    if not cleaned_texts:
        return []

    try:
        embeddings = model.encode(cleaned_texts, convert_to_tensor=True)
        return embeddings.tolist()
    except Exception as e:
        print(f"[Embedder] Batch embedding failed: {e}")
        return []
