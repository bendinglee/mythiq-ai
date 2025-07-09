def validate_feedback(data):
    required = ["input", "output", "user_feedback"]
    for field in required:
        if not data.get(field): return False
    return True
