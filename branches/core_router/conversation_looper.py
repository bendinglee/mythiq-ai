def regenerate_response(prompt):
    from branches.general_knowledge.router import answer_route
    from branches.qa_validator.routes import grade_answer
    from branches.uncertainty_detector.routes import check_uncertainty

    initial = answer_route({ "question": prompt })
    grade = grade_answer({ "input": prompt, "output": initial.get("answer", "") })
    clarity = check_uncertainty({ "content": initial.get("answer", "") })

    return {
        "response": initial.get("answer"),
        "qa_score": grade.get("score"),
        "confidence": clarity.get("score")
    }
