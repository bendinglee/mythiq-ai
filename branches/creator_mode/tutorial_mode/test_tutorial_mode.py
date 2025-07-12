from branches.tutorial_mode.tutorial_renderer import render_tutorial

def test_tutorial():
    data = render_tutorial()
    assert data["success"], "❌ Tutorial rendering failed"
    assert len(data["faq"]) > 0, "❌ FAQ missing"
    assert len(data["presets"]) > 0, "❌ Presets missing"
    print("✅ Tutorial Mode test passed.")

if __name__ == "__main__":
    test_tutorial()
