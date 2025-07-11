from branches.translation_hub.translator_engine import translate_text
from branches.translation_hub.tone_translator import rewrite_tone

def test_translation_hub():
    sample = "AI is transforming education."
    translated = translate_text(sample, "es")
    toned = rewrite_tone(translated, "excited")

    assert "Traducción" in translated, "❌ Language translation failed"
    assert "Awesome" in toned, "❌ Tone formatting failed"

    print("✅ Translation Hub test passed.")

if __name__ == "__main__":
    test_translation_hub()
