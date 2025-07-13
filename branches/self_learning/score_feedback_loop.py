from branches.qa_validator.gradebook import log_grade
from branches.uncertainty_detector.confidence_overlay import confidence_score
from branches.self_learning.log import log_entry
from branches.self_learning.reflect import generate_reflection
from branches.self_diagnostics.test_runner import run_all_tests
from branches.self_diagnostics.score_mapper import compute_score
from branches.self_tuner.tune_persona import tune_persona_settings  # 🔁 Added

def feedback_loop(payload):
    score_data = log_grade(payload, return_only=True)
    confidence_data = confidence_score(payload, return_only=True)
    reflection = generate_reflection({ **payload.get("meta", {}), **score_data })

    diagnostics = run_all_tests()
    diag_score = compute_score(diagnostics)

    enriched_meta = {
        **payload.get("meta", {}),
        "score": score_data.get("score", 0.0),
        "confidence": confidence_data.get("confidence", 0.0),
        "reflection": reflection.get("reflection", []),
        "diagnostic_score": diag_score
    }

    # 🔁 Auto-adjust persona config based on diagnostics + feedback
    tune_result = tune_persona_settings(enriched_meta)
    enriched_meta["tune_profile"] = tune_result.get("preset")

    enriched_payload = {
        **payload,
        "meta": enriched_meta
    }

    log_entry(enriched_payload)
    return enriched_payload
