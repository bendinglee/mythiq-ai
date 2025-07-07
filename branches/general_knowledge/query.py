from branches.general_knowledge.loader import get_knowledge
from flask import jsonify

def answer_general_knowledge(request):
    q = request.args.get("q", "").strip().lower()
    answer = get_knowledge(q)

    return jsonify({
        "success": True if answer else False,
        "answer": answer or "🤖 I couldn't find an answer to that yet."
    })
