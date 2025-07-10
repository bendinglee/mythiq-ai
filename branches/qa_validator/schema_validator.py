def validate_entry(entry):
    required = ["input", "output", "tags"]
    missing = [k for k in required if k not in entry]
    return { "valid": not missing, "missing": missing }
