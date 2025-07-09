import requests, os, uuid, re

HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL = "stabilityai/stable-diffusion-2"
HF_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"

STATIC_PATH = "static/generated"

def sanitize_filename(text):
    safe = re.sub(r"[^\w\s-]", "", text).strip().replace(" ", "_")
    return safe[:40]

def synthesize_image(prompt, modifiers=None):
    if not prompt:
        return { "success": False, "error": "No prompt provided." }

    headers = { "Authorization": f"Bearer {HF_TOKEN}" }
    payload = { "inputs": prompt }

    try:
        response = requests.post(HF_URL, headers=headers, json=payload)

        if response.status_code != 200 or "image" not in response.headers.get("content-type", ""):
            return {
                "success": False,
                "error": f"HF request failed: {response.text}",
                "style_applied": modifiers or "default"
            }

        # 🔐 Ensure static folder exists
        os.makedirs(STATIC_PATH, exist_ok=True)

        # 🖼️ Save image using UUID to avoid collisions
        file_id = str(uuid.uuid4())[:8]
        filename = f"{sanitize_filename(prompt)}_{file_id}.png"
        img_path = os.path.join(STATIC_PATH, filename)

        with open(img_path, "wb") as f:
            f.write(response.content)

        return {
            "success": True,
            "synth_url": f"/{img_path}",
            "style_applied": modifiers or "default"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "style_applied": modifiers or "default"
        }
