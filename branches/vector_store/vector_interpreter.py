def interpret_vector_matches(results):
    return [f"{r['text']} (score: {r['score']})" for r in results if r.get("text")]
