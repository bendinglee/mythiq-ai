from flask import request, jsonify
from branches.qa_validator.scorer import score_answer
from branches.qa_validator.gradebook import log_score

def validate_answer_route():
    try:
        data = request.get_json()
        question = data.get("question", "")
        answer = data.get("answer", "")
        source = data.get("source", "")

        score = score_answer(question, answer, source)
        log_score(question, answer, score)

        return jsonify({ "success": True, "score": score })
    except Exception as e:
        return jsonify({ "success": False, "error": str(e) }), 500
