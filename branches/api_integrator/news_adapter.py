import requests
from branches.api_integrator.auth_manager import get_api_key

def get_news_data():
    api_key = get_api_key("news")
    if not api_key:
        return { "success": False, "error": "Missing News API key." }

    try:
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
        response = requests.get(url, timeout=5)
        data = response.json()
        headlines = [a["title"] for a in data.get("articles", [])[:5]]
        return { "success": True, "headlines": headlines }
    except Exception as e:
        return { "success": False, "error": str(e) }
