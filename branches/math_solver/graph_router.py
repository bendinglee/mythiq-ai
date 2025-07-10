def route_math_query(query):
    if any(op in query for op in ["graph", "plot"]):
        from branches.math_solver.graph_engine import generate_graph
        return generate_graph(query)
    else:
        from branches.math_solver.solver import solve_math_query
        return solve_math_query(query)
