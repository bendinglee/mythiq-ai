import datetime

translation_log = []

def log_translation(original, translated, lang, tone):
    translation_log.append({
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "original": original,
        "translated": translated,
        "language": lang,
        "tone": tone
    })

def get_recent_translations(limit=5):
    return translation_log[-limit:]
