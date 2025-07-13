from branches.memory_mapper.memory_fetcher import fetch_logs
from branches.memory_mapper.score_overlay import score_tags

def build_grid():
    entries = fetch_logs()
    grid = []
    for e in entries:
        meta = e.get("meta", {})
        tags = score_tags(meta)
        grid.append({
            "id": meta.get("id"),
            "score": tags["score"],
            "confidence": tags["confidence"],
            "diagnostic": tags["diagnostic_score"],
            "tone": meta.get("emotion_tag", "neutral")
        })
    return grid
