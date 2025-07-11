def build_checklist(text):
    if not text:
        return { "success": False, "message": "Checklist text missing." }

    items = [f"• {line.strip()}" for line in text.split(",") if line.strip()]
    return {
        "success": True,
        "checklist": items,
        "title": "✅ Your generated checklist"
    }
