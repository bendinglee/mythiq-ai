import re

def clean_and_split_text(raw_text):
    # Remove multiple newlines and excess spaces
    text = re.sub(r"\n{2,}", "\n", raw_text.strip())
    text = re.sub(r"[ \t]{2,}", " ", text)

    # Simple split into chunks (e.g., paragraphs or 2–3 sentences)
    chunks = []
    current = ""
    for line in text.split("\n"):
        if len(current) + len(line) < 500:
            current += " " + line.strip()
        else:
            if current:
                chunks.append(current.strip())
            current = line.strip()
    if current:
        chunks.append(current.strip())

    return [c for c in chunks if len(c) > 20]
