import json
import os
from collections import defaultdict

LOG_PATH = "memory/feedback_logs.json"

def generate_feedback_summary():
    if not os.path.exists(LOG_PATH):
        return "📝 No feedback logs found."

    with open(LOG_PATH, "r") as f:
        logs = json.load(f)

    if not logs:
        return "📂 Feedback log is empty. No reflection data available."

    tag_groups = defaultdict(list)
    total_confidence = 0
    total_entries = len(logs)
    uncertainty_count = 0

    for entry in logs:
        total_confidence += entry.get("confidence", 0.5)
        if entry.get("confidence", 0.5) < 0.5:
            uncertainty_count += 1
        for tag in entry.get("tags", []):
            tag_groups[tag].append(entry)

    avg_conf = round(total_confidence / total_entries, 2)
    summary = [f"🧠 Mythiq Feedback Summary"]
    summary.append(f"Total feedback entries: {total_entries}")
    summary.append(f"Average confidence score: {avg_conf}")
    summary.append(f"Uncertain responses (<0.5): {uncertainty_count}")

    for tag, items in tag_groups.items():
        summary.append(f"\n🔍 Tag: {tag}")
        summary.append(f"- Entries: {len(items)}")
        if len(items) >= 3:
            summary.append(f"- Suggest improvement in '{tag}' module (recurring feedback)")
        examples = [f"• {i['input']} → {i['feedback']}" for i in items[:2]]
        summary.extend(examples)

    return "\n".join(summary)
