import requests
from branches.api_integrator.auth_manager import get_api_key

def get_weather_data(location):
    api_key = get_api_key("weather")
    if not api_key:
        return { "success": False, "error": "Missing Weather API key." }

    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
        response = requests.get(url, timeout=5)
        data = response.json()
        main = data.get("weather", [{}])[0].get("description", "No data")
        temp = data.get("main", {}).get("temp", "N/A")

        return {
            "success": True,
            "location": location,
            "description": main,
            "temperature": f"{temp}°C"
        }
    except Exception as e:
        return { "success": False, "error": str(e) }
