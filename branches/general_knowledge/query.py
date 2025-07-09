from branches.general_knowledge.loader import get_knowledge

def answer_general_knowledge(request):
    # 🔍 Handle both direct query and dispatcher input formats
    if isinstance(request, dict):
        q = request.get("args", {}).get("q", "").strip().lower()
    else:
        q = request.args.get("q", "").strip().lower()

    # 🧠 Get matched answer from loaded knowledge base
    answer = get_knowledge(q)

    # 🧾 Return structured response
    return {
        "success": True if answer else False,
        "output": answer or "🤖 I couldn't find an answer to that yet.",
        "confidence": 0.9 if answer else 0.4,
        "tags": ["general_knowledge"]
    }
