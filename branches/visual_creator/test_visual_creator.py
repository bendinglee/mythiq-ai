from branches.visual_creator.controller import create_visual_asset

def test_visual_creator():
    sample = {
        "prompt": "Castle in the clouds",
        "style": "fantasy",
        "overlay": "Welcome to Avalon"
    }
    result = create_visual_asset(**sample)
    assert result["success"] and result["image_url"], "❌ Visual creation failed."
    print(f"✅ Visual created: {result['image_url']}")

if __name__ == "__main__":
    test_visual_creator()
