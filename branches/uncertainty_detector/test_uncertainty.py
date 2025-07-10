from branches.uncertainty_detector.analyzer import detect_uncertain_phrases
from branches.uncertainty_detector.confidence_grader import grade_confidence
from branches.uncertainty_detector.uncertainty_reporter import build_report

def test_detector():
    text = "Some say AI might replace most jobs eventually."
    phrases = detect_uncertain_phrases(text)
    score = grade_confidence(text, phrases)
    report = build_report(text, phrases, score)

    print(f"Confidence Score: {score}")
    for line in report:
        print(f"- {line}")

if __name__ == "__main__":
    test_detector()
