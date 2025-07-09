import re

def extract_prompt_metadata(prompt_text):
    style = "unknown"
    modifiers = []

    style_match = re.search(r"

\[(.*?)\]

", prompt_text)
    if style_match:
        style = style_match.group(1)

    modifiers = re.findall(r"--(.*)", prompt_text)
    keywords = []
    if modifiers:
        keywords = [kw.strip() for kw in modifiers[0].split(",") if len(kw.strip()) > 0]

    return {
        "style": style,
        "modifiers": modifiers[0] if modifiers else "",
        "keywords": keywords
    }
