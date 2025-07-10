from vector_store.embedder import embed_texts
from vector_store.vector_store import load_index, save_index, load_metadata, save_metadata
import faiss, numpy as np

def ingest_texts(texts):
    embeddings = embed_texts(texts)
    index = load_index()
    for vec in embeddings:
        index.add(np.array([vec]).astype('float32'))
    save_index(index)

    metadata = load_metadata()
    for i, text in enumerate(texts):
        metadata.append({ "id": len(metadata), "text": text })
    save_metadata(metadata)

    return { "success": True, "added": len(texts) }
