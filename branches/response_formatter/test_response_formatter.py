from branches.response_formatter.tone_engine import apply_tone
from branches.response_formatter.style_selector import select_style

def test_formatter():
    sample = "AI is transforming the world."
    styled = select_style(sample, "highlight")
    toned = apply_tone(styled, "friendly")
    assert "🔍" in styled and "😊" in toned, "❌ Tone or style formatting failed."
    print("✅ Response Formatter passed.")

if __name__ == "__main__":
    test_formatter()
