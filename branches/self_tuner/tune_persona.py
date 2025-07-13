from branches.self_tuner.preset_editor import update_profile

def tune_persona_settings(meta):
    score = meta.get("score", 0.5)
    confidence = meta.get("confidence", 0.5)
    diagnostic_score = meta.get("diagnostic_score", 0.5)

    preset = "default"
    simplify = False
    tone = "friendly"

    if score < 0.4 or confidence < 0.5:
        preset = "beginner_mode"
        simplify = True
        tone = "friendly"
    elif score > 0.8 and diagnostic_score > 0.7:
        preset = "formal_expert"
        simplify = False
        tone = "serious"

    result = update_profile(preset, tone=tone, simplify=simplify)
    return { "preset": preset, "tone": tone, "simplify": simplify }
