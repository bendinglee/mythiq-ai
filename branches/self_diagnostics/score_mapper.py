def compute_score(results):
    total = len(results)
    passed = len([r for r in results if r["passed"]])
    fail_rate = 1 - (passed / total if total else 0)
    score = round(1.0 - fail_rate, 2)
    return score
