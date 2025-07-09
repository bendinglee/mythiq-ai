import json
from flask import jsonify

def render_gallery_html():
    try:
        with open("memory/image_logs.json", "r", encoding="utf-8") as f:
            logs = json.load(f)

        logs = [log for log in logs if log.get("image_url")]
        logs = sorted(logs, key=lambda x: x.get("timestamp", ""), reverse=True)
        latest = logs[-50:]

        html = "<h2>🖼️ Mythiq Gallery</h2><div style='display:grid;gap:20px;'>"
        for entry in latest:
            prompt = entry.get("crafted_prompt") or entry.get("input_prompt", "")
            img = entry.get("image_url", "")
            html += f"<div><img src='{img}' style='max-width:100%;border-radius:8px;'/><p>{prompt}</p></div>"
        html += "</div>"

        return html
    except Exception as e:
        return f"<h2>Error loading gallery:</h2><pre>{str(e)}</pre>"

def api_gallery_json():
    try:
        with open("memory/image_logs.json", "r", encoding="utf-8") as f:
            logs = json.load(f)
        return jsonify({"success": True, "logs": logs[-50:]})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
