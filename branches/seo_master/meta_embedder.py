def generate_meta_tags(topic, keywords):
    base_keywords = ", ".join(keywords)
    title = f"Discover More About {topic.title()}"
    description = f"Explore expert insights on {topic}. Learn how it works, why it matters, and what’s next in the field."
    
    meta = {
        "title": title,
        "description": description,
        "meta_tags": {
            "keywords": base_keywords,
            "og:title": title,
            "og:description": description,
            "twitter:card": "summary_large_image"
        }
    }
    return meta
