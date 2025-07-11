def generate_reminder(content):
    if not content:
        return { "success": False, "message": "No reminder content provided." }

    simulated = f"🔔 Reminder set: '{content}' (simulation only)"
    return { "success": True, "reminder": simulated }
