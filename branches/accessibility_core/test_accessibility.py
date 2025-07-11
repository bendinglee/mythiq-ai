from branches.accessibility_core.voice_captioner import generate_voice_caption
from branches.accessibility_core.alt_text_generator import describe_visual
from branches.accessibility_core.screenreader_adapter import format_for_screen_reader

def test_accessibility_core():
    vc = generate_voice_caption("Hello world")
    at = describe_visual("A spaceship flying above Earth")
    sr = format_for_screen_reader("AI is enhancing accessibility.")

    assert vc["success"] and "Spoken Output" in vc["caption"], "❌ Voice caption failed"
    assert at["success"] and "Alt Text" in at["alt_text"], "❌ Alt text failed"
    assert sr["success"] and "<sr-output" in sr["formatted"], "❌ Screen reader failed"

    print("✅ Accessibility Core test passed.")

if __name__ == "__main__":
    test_accessibility_core()
