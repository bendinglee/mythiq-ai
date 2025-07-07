from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def score_answer(question, answer, source_reference):
    try:
        if not source_reference:
            return { "confidence": 0, "match": False, "feedback": "No reference provided." }

        q_embed = model.encode(question, convert_to_tensor=True)
        a_embed = model.encode(answer, convert_to_tensor=True)
        s_embed = model.encode(source_reference, convert_to_tensor=True)

        q_a_sim = util.pytorch_cos_sim(q_embed, a_embed).item()
        a_s_sim = util.pytorch_cos_sim(a_embed, s_embed).item()

        match = q_a_sim > 0.6 and a_s_sim > 0.7
        confidence = round((q_a_sim + a_s_sim) / 2, 3)

        return {
            "confidence": confidence,
            "match": match,
            "similarity_to_question": round(q_a_sim, 3),
            "similarity_to_source": round(a_s_sim, 3),
            "feedback": "Answer matches source." if match else "Possible mismatch or hallucination."
        }

    except Exception as e:
        return { "confidence": 0, "match": False, "feedback": f"Error: {e}" }
