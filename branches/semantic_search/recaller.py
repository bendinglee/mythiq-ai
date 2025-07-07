from branches.semantic_search.embedder import embed_text
from branches.semantic_search.vector_store import load_index, search_index, load_knowledge_pairs

def recall_fuzzy_answer(query):
    vec = embed_text(query)
    index = load_index()
    matches = search_index(index, vec, k=1)

    data = load_knowledge_pairs()
    if matches[0] < len(data):
        return data[matches[0]]["answer"]
    return None
