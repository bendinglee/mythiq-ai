from sentence_transformers import SentenceTransformer

_model = None

def get_embedder():
    global _model
    if _model is None:
        _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return _model

def embed_text(text):
    model = get_embedder()
    return model.encode([text])[0]

def embed_texts(texts, model=None):
    if model is None:
        model = get_embedder()
    return model.encode(texts, convert_to_tensor=True)
