def validate_schema(data):
    if "records" not in data or not isinstance(data["records"], list):
        return False, "Missing or invalid 'records' array."

    for item in data["records"]:
        if "text" not in item or not isinstance(item["text"], str):
            return False, "Each record must have a 'text' string."
        if "tags" in item and not isinstance(item["tags"], list):
            return False, "'tags' must be a list if present."

    return True, "Schema valid."
