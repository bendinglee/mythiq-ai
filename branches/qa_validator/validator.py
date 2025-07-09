def validate_entry(data):
    errors = []
    if not data.get("input"): errors.append("Missing input.")
    if not data.get("output"): errors.append("Missing output.")
    return { "valid": len(errors) == 0, "errors": errors }
