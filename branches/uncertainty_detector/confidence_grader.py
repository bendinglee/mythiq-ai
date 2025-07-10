def grade_confidence(text, matched_phrases):
    word_count = len(text.split())
    hedge_penalty = len(matched_phrases) * 0.05
    base_score = max(0.0, 1.0 - hedge_penalty)
    if word_count < 30: base_score -= 0.1
    return round(max(0.0, base_score), 2)
