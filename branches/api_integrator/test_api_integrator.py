from branches.api_integrator.news_adapter import get_news_data
from branches.api_integrator.weather_adapter import get_weather_data
from branches.api_integrator.finance_adapter import get_finance_data

def test_api_core():
    news = get_news_data()
    weather = get_weather_data("Tokyo")
    finance = get_finance_data("AAPL")

    print("✅ News:", news.get("success"))
    print("✅ Weather:", weather.get("success"))
    print("✅ Finance:", finance.get("success"))

if __name__ == "__main__":
    test_api_core()
