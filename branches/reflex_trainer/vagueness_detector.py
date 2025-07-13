def is_vague(text):
    vague = ["I guess", "maybe", "sort of", "kind of", "probably"]
    return any(v in text.lower() for v in vague)
