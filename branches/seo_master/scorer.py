import re

def score_seo_strength(text, keywords):
    text = text.strip().lower()
    text_words = re.findall(r'\b\w+\b', text)
    total_words = len(text_words)

    if not text_words or not keywords:
        return {
            "score": 0.0,
            "grade": "none",
            "keyword_match_count": 0,
            "density": 0.0,
            "total_keywords": len(keywords),
            "markup_flags": [],
            "feedback": ["🟡 Missing keywords or content."],
            "keyword_density": 0.0
        }

    hits = sum(1 for word in text_words if word in [kw.lower() for kw in keywords])
    density = hits / total_words
    markup_flags = []

    if "<title>" in text or "<h1>" in text:
        markup_flags.append("title tag present")
    if "meta name=" in text or "description" in text:
        markup_flags.append("meta tags present")

    score = 0.0
    feedback = []

    if density > 0.2:
        score += 0.3
        grade = "excellent"
        feedback.append("✅ Strong keyword density.")
    elif density > 0.1:
        score += 0.2
        grade = "good"
        feedback.append("🧠 Moderate keyword usage.")
    else:
        grade = "low"
        feedback.append("⚠️ Weak keyword presence.")

    if len(text) > 500:
        score += 0.2
        feedback.append("📄 Good content length.")

    if markup_flags:
        score += 0.2
        feedback.append("🔖 Markup tags detected.")

    return {
        "score": round(score, 2),
        "grade": grade,
        "keyword_match_count": hits,
        "density": round(density, 3),
        "total_keywords": len(keywords),
        "markup_flags": markup_flags,
        "feedback": feedback,
        "keyword_density": round(density * 100, 2)
    }
