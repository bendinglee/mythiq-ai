import json
import os
from datetime import datetime

LOG_PATH = "memory/image_logs.json"

def save_image_log(prompt, url):
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w") as f:
            json.dump([], f)

    with open(LOG_PATH, "r") as f:
        logs = json.load(f)

    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "input_prompt": prompt,
        "image_url": url,
        "tags": ["image", "synthesized"]
    }

    logs.append(entry)

    with open(LOG_PATH, "w") as f:
        json.dump(logs, f, indent=2)
