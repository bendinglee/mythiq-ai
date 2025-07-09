def safe_parse_fallback(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception as e:
        return f"❌ Unable to parse fallback: {str(e)}"
