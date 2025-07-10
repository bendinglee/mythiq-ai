import re
from collections import Counter

# 🛡️ Basic stopwords (can extend by language later)
stopwords = set([
    "the", "and", "or", "a", "an", "this", "that", "in", "on", "for", "with",
    "of", "to", "is", "are", "as", "at", "by", "from", "be", "it", "was", "were"
])

def extract_keywords(text, max_keywords=8):
    if not isinstance(text, str) or not text.strip():
        return []

    # ✂️ Tokenize and filter
    words = re.findall(r"\b\w+\b", text.lower())
    filtered = [w for w in words if w not in stopwords and len(w) > 2 and w.isalpha()]

    # 📊 Frequency count
    counts = Counter(filtered)
    sorted_keywords = [word for word, _ in counts.most_common(max_keywords)]

    return sorted_keywords
