import requests
import os

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_ID = "stabilityai/stable-diffusion-xl-base-1.0"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"

def generate_image_from_prompt(prompt):
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Accept": "application/json"
    }

    payload = { "inputs": prompt }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        content_type = response.headers.get("Content-Type", "")
        if "image" in content_type:
            # Save locally for testing, production could use S3/IPFS/CDN
            filename = "output_image.png"
            with open(f"static/{filename}", "wb") as f:
                f.write(response.content)
            return f"/static/{filename}"
        else:
            try:
                result = response.json()
                if isinstance(result, list) and "generated_image" in result[0]:
                    return result[0]["generated_image"]
                return result
            except:
                return "✅ Image generated, but couldn’t parse metadata."
    else:
        raise Exception(f"HF API failed: {response.status_code} - {response.text}")
