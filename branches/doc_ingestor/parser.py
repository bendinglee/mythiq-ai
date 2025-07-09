import os
import re

# Optional fallback in case of encoding issues
def safe_parse_fallback(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception as e:
        return f"❌ Unable to parse fallback: {str(e)}"

def load_document(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            raw_text = f.read()
    except Exception:
        raw_text = safe_parse_fallback(file_path)

    return raw_text

def clean_and_split_text(raw_text, max_chunk_size=500):
    # Normalize spacing and newlines
    text = re.sub(r"\n{2,}", "\n", raw_text.strip())
    text = re.sub(r"[ \t]{2,}", " ", text)

    # Basic chunking: combine lines until max size reached
    chunks = []
    current = ""
    for line in text.split("\n"):
        line = line.strip()
        if len(current) + len(line) < max_chunk_size:
            current += " " + line
        else:
            if current:
                chunks.append(current.strip())
            current = line
    if current:
        chunks.append(current.strip())

    return [c for c in chunks if len(c) > 20]

def parse_document(file_path):
    raw = load_document(file_path)
    chunks = clean_and_split_text(raw)
    return chunks
