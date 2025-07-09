import requests
import os

HF_TOKEN = os.getenv("HF_TOKEN")

def generate_image_from_prompt(prompt):
    # HuggingFace Inference API (Stable Diffusion)
    url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": prompt}

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"HF request failed: {response.text}")

    # Save image binary to static folder
    img_path = f"static/generated/{prompt.replace(' ', '_')[:40]}.png"
    with open(img_path, "wb") as f:
        f.write(response.content)

    return f"/{img_path}"
