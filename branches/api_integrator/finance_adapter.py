import requests
from branches.api_integrator.auth_manager import get_api_key

def get_finance_data(ticker):
    api_key = get_api_key("finance")
    if not api_key:
        return { "success": False, "error": "Missing Finance API key." }

    try:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={api_key}"
        response = requests.get(url, timeout=5)
        data = response.json()
        quote = data.get("Global Quote", {})
        return {
            "success": True,
            "symbol": ticker,
            "price": quote.get("05. price", "N/A"),
            "change": quote.get("10. change percent", "N/A")
        }
    except Exception as e:
        return { "success": False, "error": str(e) }
