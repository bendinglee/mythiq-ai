def check_bias_phrases(text):
    bias_terms = ["always", "never", "clearly", "everyone knows"]
    return [term for term in bias_terms if term in text.lower()]
