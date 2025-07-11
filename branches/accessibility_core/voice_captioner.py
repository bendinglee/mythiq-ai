def generate_voice_caption(text):
    if not text:
        return { "success": False, "caption": "❌ No input provided." }

    caption = f"🎙️ Spoken Output: '{text}'"
    return { "success": True, "caption": caption }
