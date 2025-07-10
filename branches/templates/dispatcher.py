def route_request(intent, payload):
    from branches.math_solver.router import solve_math_route
    from branches.semantic_search.query_router import semantic_query_route
    # Extendable mapping
    routes = {
        "solve_math": solve_math_route,
        "semantic_search": semantic_query_route
    }
    if intent in routes:
        return routes[intent](payload)
    else:
        return { "success": False, "error": f"No route for intent: {intent}" }
