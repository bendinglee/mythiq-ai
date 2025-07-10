import re

def generate_meta_tags(topic, keywords):
    # 🧼 Clean and prepare keywords
    filtered = [kw.strip().lower() for kw in keywords if isinstance(kw, str) and len(kw.strip()) > 2]
    unique_keywords = sorted(set(filtered), key=filtered.index)
    base_keywords = ", ".join(unique_keywords)

    # ✨ Generate title & description
    safe_topic = re.sub(r'[^\w\s]', '', topic).title()
    title = f"Discover More About {safe_topic}"
    description = f"Explore expert insights on {safe_topic}. Learn how it works, why it matters, and what’s next in the field."

    # 🏷️ SEO-friendly meta tags
    meta = {
        "title": title,
        "description": description,
        "meta_tags": {
            "keywords": base_keywords,
            "og:title": title,
            "og:description": description,
            "twitter:title": title,
            "twitter:description": description,
            "twitter:card": "summary_large_image",
            "robots": "index, follow"
        }
    }

    return meta
