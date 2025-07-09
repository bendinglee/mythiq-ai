def detect_common_failure_patterns(query):
    query = query.strip().lower()
    hints = []

    if "solve for" not in query and "=" in query:
        hints.append("Add 'solve for x' for better detection.")

    if not any(op in query for op in ["+", "-", "*", "/", "="]):
        hints.append("Query lacks operators — try a complete expression.")

    if "^" in query and "**" not in query:
        hints.append("Replace '^' with '**' for exponent parsing.")

    return {
        "success": False,
        "error": "⚠️ Query format unclear or unsupported.",
        "hints": hints,
        "suggested_fix": query.replace("^", "**") + " for x" if "=" in query else None
    }
