from flask import request, jsonify
from branches.seo_master.analyzer import extract_keywords
from branches.seo_master.meta_embedder import generate_meta_tags
from branches.seo_master.scorer import score_seo_strength

def optimize_keywords_route():
    try:
        data = request.get_json()
        topic = data.get("topic", "").strip()
        if not topic:
            return jsonify({ "success": False, "error": "No topic provided." }), 400

        keywords = extract_keywords(topic)
        meta = generate_meta_tags(topic, keywords)
        seo_score = score_seo_strength(topic, keywords)

        return jsonify({
            "success": True,
            "title": meta["title"],
            "description": meta["description"],
            "keywords": keywords,
            "meta_tags": meta["meta_tags"],
            "score": seo_score
        })
    except Exception as e:
        return jsonify({ "success": False, "error": str(e) }), 500
