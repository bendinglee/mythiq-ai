def route_to_module(intent, query):
    if intent == "math":
        from branches.math_solver.solver import solve_math_query
        return { "output": solve_math_query(query), "confidence": 0.9 }

    elif intent == "image":
        from branches.image_generator.routes import generate_image_route
        return generate_image_route()

    # Add more branches as needed
    return { "output": "Intent not recognized", "confidence": 0.2 }
