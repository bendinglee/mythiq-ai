reflection_log = []

def reflect_output(entry):
    score = entry.get("score", 0)
    feedback = "Needs improvement." if score < 0.5 else "Well done!"
    reflection_log.append({ "input": entry["input"], "score": score, "feedback": feedback })

def get_reflections():
    return reflection_log
