from branches.qa_validator.gradebook import log_grade
from branches.uncertainty_detector.confidence_overlay import confidence_score
from branches.self_learning.log import log_entry
from branches.self_learning.reflect import generate_reflection
from branches.self_diagnostics.test_runner import run_all_tests
from branches.self_diagnostics.score_mapper import compute_score
from branches.self_tuner.tune_persona import tune_persona_settings  # 🔁 Added
import traceback

def feedback_loop(payload):
    try:
        # 🎯 Defensive extraction
        meta = payload.get("meta", {})
        score_data = log_grade(payload, return_only=True) or {}
        confidence_data = confidence_score(payload, return_only=True) or {}

        # 🪞 Reflection processing
        reflection_input = { **meta, **score_data }
        reflection = generate_reflection(reflection_input) or {}

        # 🧪 Self-diagnostics scoring
        diagnostics = run_all_tests() or {}
        diag_score = compute_score(diagnostics)

        # 🔁 Persona tuning
        enriched_meta = {
            **meta,
            "score": score_data.get("score", 0.0),
            "confidence": confidence_data.get("confidence", 0.0),
            "reflection": reflection.get("reflection", []),
            "diagnostic_score": diag_score
        }

        tune_result = tune_persona_settings(enriched_meta) or {}
        enriched_meta["tune_profile"] = tune_result.get("preset", "default")

        # 🧠 Final enriched output
        enriched_payload = {
            **payload,
            "meta": enriched_meta
        }

        log_entry(enriched_payload)
        return enriched_payload

    except Exception as e:
        # 🛡️ If any module fails, log and fail gracefully
        error_trace = traceback.format_exc()
        fallback_payload = {
            "success": False,
            "error": str(e),
            "trace": error_trace,
            "meta": { "diagnostic_score": 0.0, "tune_profile": "safe_fallback" }
        }
        log_entry(fallback_payload)
        return fallback_payload
