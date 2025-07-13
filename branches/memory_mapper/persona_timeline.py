from branches.memory_mapper.memory_fetcher import fetch_logs

def get_timeline():
    timeline = []
    for entry in fetch_logs():
        meta = entry.get("meta", {})
        timeline.append({
            "timestamp": meta.get("time"),
            "preset": meta.get("preset"),
            "emotion": meta.get("emotion_tag"),
            "score": meta.get("score", 0),
            "simplify": meta.get("simplify")
        })
    return timeline
