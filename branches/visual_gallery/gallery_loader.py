import json, os

GALLERY_PATH = "memory/gallery_index.json"

def load_gallery():
    if not os.path.exists(GALLERY_PATH):
        return []
    with open(GALLERY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
