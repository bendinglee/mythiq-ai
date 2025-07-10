from flask import Blueprint, request, jsonify
from branches.seo_master.analyzer import extract_keywords
from branches.seo_master.meta_embedder import generate_meta_tags
from branches.seo_master.scorer import score_seo_strength

seo_api = Blueprint("seo_master", __name__)

@seo_api.route("/api/seo-optimize", methods=["POST"])
def optimize_keywords_route():
    try:
        data = request.get_json()
        topic = data.get("topic", "").strip()
        content = data.get("content", "").strip()
        custom_keywords = data.get("keywords", [])

        if not topic and not content:
            return jsonify({
                "success": False,
                "error": "No topic or content provided."
            }), 400

        # 🧠 Determine base text to analyze
        source_text = content or topic

        # 🏷️ Extract or reuse keywords
        keywords = custom_keywords if custom_keywords else extract_keywords(source_text)

        # 🧬 Generate metadata
        meta = generate_meta_tags(source_text, keywords)

        # 🧪 SEO scoring
        score = score_seo_strength(source_text, keywords)

        return jsonify({
            "success": True,
            "input": source_text,
            "keywords": keywords,
            "meta_tags": meta.get("meta_tags", {}),
            "title": meta.get("title"),
            "description": meta.get("description"),
            "score": score.get("score"),
            "feedback": score.get("feedback"),
            "analysis": {
                "length": len(source_text),
                "keyword_density": score.get("keyword_density"),
                "markup_detected": score.get("markup_flags", [])
            }
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"SEO optimization failed: {str(e)}"
        }), 500
