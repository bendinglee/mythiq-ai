def explain_branch(name):
    glossary = {
        "math_solver": "Solves math queries including algebra, graphing, and equations.",
        "qa_validator": "Grades answer quality for clarity and correctness.",
        "semantic_search": "Finds related facts, memory, and context matches.",
        "image_generator": "Creates generative visuals from prompt text.",
        "core_router": "Dispatches user prompts to the right module.",
        "self_learning": "Learns from feedback scores and updates behavior."
    }
    return glossary.get(name, f"❓ No explanation found for '{name}'.")
