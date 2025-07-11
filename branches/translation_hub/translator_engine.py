def translate_text(text, target_lang):
    # Simulated engine: swap with HuggingFace or external API later
    if target_lang == "es":
        return f"Traducción simulada: '{text}' en Español"
    elif target_lang == "fr":
        return f"Traduction simulée: '{text}' en Français"
    elif target_lang == "de":
        return f"Übersetzung simuliert: '{text}' auf Deutsch"
    elif target_lang == "jp":
        return f"日本語での翻訳: '{text}'"
    elif target_lang == "zh":
        return f"翻译结果（中文）: '{text}'"
    else:
        return f"[EN] {text}"  # Default fallback to English
