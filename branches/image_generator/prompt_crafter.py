def stylize_prompt(base_prompt, style="cinematic"):
    # 🔁 Style aliases
    aliases = {
        "photo": "photorealistic",
        "realistic": "photorealistic",
        "ghibli": "anime",
        "dark": "cinematic",
        "epic": "fantasy"
    }

    # 🎨 Style suffixes
    suffixes = {
        "cinematic": " --ultra detailed, wide angle, epic lighting, 8K, sharp focus",
        "anime": " --anime style, vibrant tones, Studio Ghibli look, cel-shaded",
        "fantasy": " --medieval fantasy, glowing particles, soft lighting, ethereal",
        "photorealistic": " --hyperreal, 35mm, full depth, cinematic shadows",
        "comic": " --inked outlines, bold contrast, comic style, dynamic pose"
    }

    normalized = aliases.get(style.lower(), style.lower())
    modifier = suffixes.get(normalized, suffixes["cinematic"])
    prompt = f"{base_prompt.strip()} {modifier}".strip()

    # 🧾 Tag the style in prompt for memory log or audit trail
    return f"[{normalized}] {prompt}"
