def score_seo_strength(text, keywords):
    text_words = text.lower().split()
    hits = sum(1 for word in text_words if word in keywords)
    density = hits / len(text_words) if text_words else 0
    return {
        "density": round(density, 3),
        "keyword_match_count": hits,
        "total_keywords": len(keywords),
        "grade": "excellent" if density > 0.2 else "good" if density > 0.1 else "low"
    }
