from branches.persona_settings.persona_tuner import apply_persona_tuning

def test_persona_settings():
    sample = "In summary, AI models adapt based on feedback."
    beginner = apply_persona_tuning(sample, "beginner_mode")
    assert "😊" in beginner or "•" in beginner, "❌ Beginner tone/styling failed"

    formal = apply_persona_tuning(sample, "formal_expert")
    assert "🔍" in formal or "In summary" in formal, "❌ Formal tone missing"

    print("✅ Persona Settings test passed.")

if __name__ == "__main__":
    test_persona_settings()
