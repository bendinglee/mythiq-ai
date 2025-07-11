def validate_entry(entry):
    required = ["image_url", "style", "source"]
    missing = [k for k in required if k not in entry]
    return { "valid": not missing, "missing": missing }
