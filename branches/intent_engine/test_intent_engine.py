from branches.intent_engine.intent_classifier import classify_intent
from branches.intent_engine.intent_resolver import resolve_intent

def test_intent():
    sample = "Can you draw an owl in space?"
    raw = classify_intent(sample)
    final = resolve_intent(raw)

    assert final["intent"] in ["generate_image", "image_generator"], "❌ Intent resolution failed."
    print("✅ Intent engine test passed.")

if __name__ == "__main__":
    test_intent()
