import json, os

MANIFEST_PATH = os.path.join(os.path.dirname(__file__), "store_manifest.json")

def list_store_plugins():
    if not os.path.exists(MANIFEST_PATH):
        return []

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)
        return manifest.get("packs", [])
