from vector_store.embedder import embed_texts
from vector_store.vector_store import load_index, load_metadata, search_index

def query_vector_store(query):
    index = load_index()
    metadata = load_metadata()
    embedding = embed_texts([query])[0]
    results = search_index(index, embedding)

    enriched = []
    for r in results:
        entry = next((m for m in metadata if m["id"] == r["id"]), {})
        enriched.append({ "text": entry.get("text", ""), "score": r["score"] })

    return { "success": True, "query": query, "results": enriched }
