from branches.self_learning.routes import reflect
from branches.qa_validator.routes import grade_answer
from branches.uncertainty_detector.routes import check_uncertainty

def trigger_global_reflection():
    sample = {
        "input": "What is gravity?",
        "output": "Gravity is a force of attraction between masses."
    }

    reflection = reflect(sample)
    qa = grade_answer(sample)
    uncertainty = check_uncertainty({ "content": sample["output"] })

    return {
        "success": True,
        "qa_score": qa.get("score"),
        "reflection": reflection,
        "confidence": uncertainty.get("score")
    }
