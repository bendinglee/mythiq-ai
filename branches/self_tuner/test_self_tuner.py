from branches.self_tuner.tune_persona import tune_persona_settings

def test_tuner():
    meta = { "score": 0.3, "confidence": 0.4, "diagnostic_score": 0.5 }
    beginner = tune_persona_settings(meta)
    assert beginner["preset"] == "beginner_mode", "❌ Beginner mode failed"

    meta2 = { "score": 0.9, "confidence": 0.9, "diagnostic_score": 0.8 }
    expert = tune_persona_settings(meta2)
    assert expert["preset"] == "formal_expert", "❌ Expert mode failed"

    print("✅ Self Tuner test passed.")

if __name__ == "__main__":
    test_tuner()
