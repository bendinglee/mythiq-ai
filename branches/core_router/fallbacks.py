def fallback_router(query):
    try:
        # Prefer general knowledge first
        from branches.general_knowledge.query import answer_general_knowledge
        response = answer_general_knowledge({"args": {"q": query}})
        if response.get("output"): return response
    except:
        pass

    try:
        # Then semantic search fallback
        from branches.semantic_search.query_router import query_fuzzy_route
        return query_fuzzy_route(query)
    except:
        pass

    return { "output": "Fallback route failed.", "confidence": 0.0 }
