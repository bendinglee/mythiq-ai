from branches.qa_validator.gradebook import log_grade
from branches.uncertainty_detector.confidence_overlay import confidence_score
from branches.self_learning.log import log_entry
from branches.self_learning.reflect import generate_reflection

def feedback_loop(payload):
    score_data = log_grade(payload, return_only=True)
    confidence_data = confidence_score(payload, return_only=True)
    reflection = generate_reflection({ **payload.get("meta", {}), **score_data })

    enriched_payload = {
        **payload,
        "meta": {
            **payload.get("meta", {}),
            "score": score_data.get("score", 0.0),
            "confidence": confidence_data.get("confidence", 0.0),
            "reflection": reflection.get("reflection", [])
        }
    }

    log_entry(enriched_payload)
    return enriched_payload
