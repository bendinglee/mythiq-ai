def stylize_prompt(base_prompt, style="cinematic"):
    suffixes = {
        "cinematic": " --ultra detailed, wide angle, epic lighting, 8K, sharp focus",
        "anime": " --anime style, vibrant tones, Studio Ghibli look, cel-shaded",
        "fantasy": " --medieval fantasy, glowing particles, soft lighting, ethereal",
        "photorealistic": " --hyperreal, 35mm, full depth, cinematic shadows",
        "comic": " --inked outlines, bold contrast, comic style, dynamic pose"
    }

    modifier = suffixes.get(style.lower(), suffixes["cinematic"])
    return f"{base_prompt.strip()} {modifier}".strip()
