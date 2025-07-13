def apply_feedback(entry, improved, emotion):
    entry["output"] = improved
    entry["meta"]["emotion_tag"] = emotion
    return entry
