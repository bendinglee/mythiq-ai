from branches.visual_creator.controller import create_visual_asset

def test_visual():
    result = create_visual_asset("A futuristic cityscape", "cyberpunk", "Welcome to NeoTokyo")
    assert result["success"] and result["image_url"], "❌ Visual creation failed."
    print("✅ Visual creator test passed.")

if __name__ == "__main__":
    test_visual()
