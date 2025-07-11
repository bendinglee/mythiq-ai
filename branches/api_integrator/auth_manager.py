import os

def get_api_key(service):
    env_map = {
        "news": "NEWS_API_KEY",
        "weather": "WEATHER_API_KEY",
        "finance": "FINANCE_API_KEY"
    }
    return os.getenv(env_map.get(service, ""), "")
