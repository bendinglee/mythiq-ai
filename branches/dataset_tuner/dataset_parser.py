def parse_dataset(data):
    entries = []
    for item in data.get("records", []):
        entry = {
            "text": item.get("text", "").strip(),
            "tags": item.get("tags", []),
            "source": item.get("source", "manual")
        }
        entries.append(entry)
    return entries
