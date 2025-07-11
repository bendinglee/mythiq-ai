from flask import Blueprint, request, jsonify
from branches.api_integrator.news_adapter import get_news_data
from branches.api_integrator.weather_adapter import get_weather_data
from branches.api_integrator.finance_adapter import get_finance_data

api_data_api = Blueprint("api_integrator", __name__)

@api_data_api.route("/api/get-news", methods=["GET"])
def fetch_news():
    return jsonify(get_news_data())

@api_data_api.route("/api/get-weather", methods=["GET"])
def fetch_weather():
    location = request.args.get("location", "London")
    return jsonify(get_weather_data(location))

@api_data_api.route("/api/get-finance", methods=["GET"])
def fetch_finance():
    ticker = request.args.get("ticker", "MSFT")
    return jsonify(get_finance_data(ticker))
