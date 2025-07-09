import json, os, uuid, datetime

LOG_PATH = "memory/image_logs.json"

def log_synth_output(prompt, result, modifiers=None):
    # 🧠 Initialize log file if missing
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w") as f:
            json.dump([], f)

    # 📥 Read existing logs
    with open(LOG_PATH, "r") as f:
        logs = json.load(f)

    # 🖼️ Extract filename from image URL
    image_url = result.get("synth_url", "")
    filename = os.path.basename(image_url) if image_url else None

    entry = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "input_prompt": prompt,
        "image_url": image_url,
        "filename": filename,
        "style": result.get("style_applied", "default"),
        "modifiers": modifiers,
        "status": "success" if result.get("success") else "fail",
        "tags": ["image", "synthesized"]
    }

    # 📦 Append and save
    logs.append(entry)
    with open(LOG_PATH, "w") as f:
        json.dump(logs, f, indent=2)
