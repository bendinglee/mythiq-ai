import json, os, re

PHRASE_DB = os.path.join(os.path.dirname(__file__), "phrase_bank.json")

def load_uncertainty_phrases():
    """Load hedge/vague phrases from phrase bank."""
    if not os.path.exists(PHRASE_DB):
        return []
    try:
        with open(PHRASE_DB, "r", encoding="utf-8") as f:
            phrases = json.load(f)
            return [p.strip().lower() for p in phrases if isinstance(p, str)]
    except Exception as e:
        print(f"[Analyzer] Failed to load phrase bank: {e}")
        return []

def assess_uncertainty(response_obj):
    """Detect uncertainty markers and return confidence status."""
    output = response_obj.get("output", "")
    confidence = float(response_obj.get("confidence", 1.0))

    normalized = output.lower()
    phrases = load_uncertainty_phrases()

    matched = []
    for phrase in phrases:
        if re.search(r"\b" + re.escape(phrase) + r"\b", normalized):
            matched.append(phrase)

    is_uncertain = bool(matched) or confidence < 0.6

    return {
        "is_uncertain": is_uncertain,
        "confidence_score": round(confidence, 2),
        "matched_phrases": matched
    }
