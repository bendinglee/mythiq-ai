from branches.creator_mode.creator_orchestrator import trigger_creation

def test_creator():
    result_img = trigger_creation("A floating island above the clouds", "image", "dreamy")
    assert result_img.get("success", False), "❌ Image generation failed"

    result_vid = trigger_creation("A cyberpunk city timelapse", "video", "cinematic")
    assert result_vid.get("success", False), "❌ Video generation failed"

    print("✅ Creator Mode test passed.")

if __name__ == "__main__":
    test_creator()
