from branches.memory_core.scorer import score_memory_entry
from branches.qa_validator.scorer import score_response

def test_score_consistency():
    memory_entry = {
        "input": "Explain gravity",
        "output": "Gravity is a force of attraction...",
        "tags": ["physics", "science"],
        "success": True,
        "meta": { "reflection_weight": 0.2 }
    }

    qa_entry = {
        "input": "Explain gravity",
        "output": "Gravity is a force of attraction between objects.",
        "tags": ["physics"]
    }

    mem_score = score_memory_entry(memory_entry)
    qa_score = score_response(qa_entry)["score"]

    print(f"🧠 Memory score: {mem_score}")
    print(f"📊 QA score: {qa_score}")

    if abs(mem_score - qa_score) < 0.5:
        print("✅ Scores are aligned.")
    else:
        print("⚠️ Score mismatch detected.")

if __name__ == "__main__":
    test_score_consistency()
