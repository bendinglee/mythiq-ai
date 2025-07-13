from branches.self_diagnostics.test_runner import run_all_tests
from branches.self_diagnostics.score_mapper import compute_score

def test_self_diag():
    results = run_all_tests()
    score = compute_score(results)

    assert isinstance(score, float), "❌ Score not a float"
    assert score >= 0 and score <= 1.0, "❌ Score out of range"
    assert len(results) > 0, "❌ No test results found"

    print(f"✅ Self Diagnostics passed with score: {score}")

if __name__ == "__main__":
    test_self_diag()
