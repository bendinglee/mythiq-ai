from sentence_transformers import SentenceTransformer
import torch

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return _model

def embed_texts(texts, model=None):
    model = model or get_model()
    cleaned = [str(t).strip() for t in texts if isinstance(t, str) and t.strip()]
    return model.encode(cleaned, convert_to_tensor=True).tolist()
