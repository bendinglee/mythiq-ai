import re
from collections import Counter

stopwords = set([
    "the", "and", "or", "a", "an", "this", "that", "in", "on", "for", "with", "of", "to", "is", "are", "as", "at"
])

def extract_keywords(text, max_keywords=8):
    words = re.findall(r"\b\w+\b", text.lower())
    words = [w for w in words if w not in stopwords and len(w) > 2]
    counts = Counter(words)
    sorted_keywords = [word for word, _ in counts.most_common(max_keywords)]
    return sorted_keywords
