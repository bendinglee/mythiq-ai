from branches.visual_gallery.controller import load_gallery

def test_gallery():
    gallery = load_gallery()
    assert isinstance(gallery, list), "❌ Gallery failed to load."
    print("✅ Gallery test passed.")

if __name__ == "__main__":
    test_gallery()
