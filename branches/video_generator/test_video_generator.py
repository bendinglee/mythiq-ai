from branches.video_generator.controller import generate_video_clip

def test_video():
    result = generate_video_clip("AI in space", "cinematic", 5)
    assert result["success"] and result["video_url"], "❌ Video generation failed."
    print("✅ Video generator test passed.")

if __name__ == "__main__":
    test_video()
