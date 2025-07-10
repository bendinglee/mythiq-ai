def fallback_dispatch(intent, payload):
    from branches.semantic_search.query_router import semantic_query_route
    from branches.general_knowledge.router import answer_route

    try:
        result = semantic_query_route(payload)
        if result.get("success"):
            return result
    except:
        pass

    try:
        return answer_route(payload)
    except:
        return { "success": False, "error": "All fallback paths failed." }
