import json, os, datetime

GALLERY_PATH = "memory/image_gallery.json"

def archive_image(entry):
    if not os.path.exists(GALLERY_PATH):
        with open(GALLERY_PATH, "w") as f:
            json.dump([], f)

    with open(GALLERY_PATH, "r") as f:
        logs = json.load(f)

    logs.append({
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "filename": entry.get("filename"),
        "image_url": entry.get("image_url"),
        "prompt": entry.get("input_prompt"),
        "style": entry.get("style"),
        "tags": entry.get("tags", [])
    })

    with open(GALLERY_PATH, "w") as f:
        json.dump(logs, f, indent=2)
