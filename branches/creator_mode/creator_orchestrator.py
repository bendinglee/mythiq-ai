import requests
import json, os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "creator_config.json")

def load_presets():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def trigger_creation(prompt, mode, style):
    presets = load_presets()
    style_map = presets.get("style_map", {})
    style_params = style_map.get(style, {})

    payload = { "prompt": prompt, **style_params }

    try:
        if mode == "image":
            res = requests.post("http://localhost:5000/api/generate-image", json=payload)
        elif mode == "video":
            res = requests.post("http://localhost:5000/api/generate-video", json=payload)
        elif mode == "visual":
            res = requests.post("http://localhost:5000/api/visual-creator", json=payload)
        else:
            return { "success": False, "error": f"Unsupported mode: {mode}" }

        return res.json()
    except Exception as e:
        return { "success": False, "error": str(e) }
