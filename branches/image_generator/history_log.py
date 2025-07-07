import json
import os
from datetime import datetime

LOG_FILE = "memory/image_logs.json"

def log_image_generation(raw_prompt, final_prompt, style, image_url):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "style": style,
        "input_prompt": raw_prompt,
        "crafted_prompt": final_prompt,
        "image_url": image_url
    }

    os.makedirs("memory", exist_ok=True)
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
    else:
        history = []

    history.append(entry)

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)
