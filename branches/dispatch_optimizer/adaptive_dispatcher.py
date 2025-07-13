from branches.intent_router.classifier import classify_intent
from branches.self_diagnostics.test_runner import run_all_tests
from branches.self_diagnostics.score_mapper import compute_score
from branches.plugin_dispatcher.plugin_loader import available_plugins
from branches.dispatch_optimizer.intent_weight_mapper import map_intent_to_task

def dynamic_dispatch(payload):
    text = payload.get("input", "")
    intent = classify_intent({ "text": text })
    confidence = intent.get("confidence", 0.5)
    label = intent.get("intent", "unknown")

    diagnostics = run_all_tests()
    diag_score = compute_score(diagnostics)

    plugins = available_plugins()
    plugin_names = [p["name"] for p in plugins]

    target_task = map_intent_to_task(label, confidence, diag_score, plugin_names)

    return {
        "intent_label": label,
        "confidence": confidence,
        "diagnostic_score": diag_score,
        "available_plugins": plugin_names,
        "routed_task": target_task
    }
