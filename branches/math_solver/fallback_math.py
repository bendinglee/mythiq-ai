def detect_and_rewrite_failed_query(query):
    query = query.strip().lower()
    suggestions = []
    fixed = query

    if "=" in query and "solve for" not in query:
        fixed += " solve for x"
        suggestions.append("🔁 Added 'solve for x' to clarify equation.")

    if "^" in query and "**" not in query:
        fixed = fixed.replace("^", "**")
        suggestions.append("🔁 Replaced '^' with '**' for exponent syntax.")

    if not any(op in query for op in ["+", "-", "*", "/", "="]):
        suggestions.append("⚠️ Query may lack mathematical operators.")

    return {
        "success": True,
        "original": query,
        "rewritten": fixed.strip(),
        "hints": suggestions or ["✅ Format appears acceptable."]
    }
