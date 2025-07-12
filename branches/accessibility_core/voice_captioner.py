def generate_voice_caption(text):
    if not text:
        return { "success": False, "caption": "📭 No content to speak." }
    return { "success": True, "caption": f"🎙️ Speaking: '{text}'" }
