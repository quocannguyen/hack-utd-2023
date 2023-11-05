from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv
from sentimentanalysis import get_articles_sentiments
from generativeai import generate_symbols, generate_analysis
import json

load_dotenv(".env")
app = Flask(__name__)
cors = CORS(app)
app.config.from_pyfile("settings.py")

@app.route("/api/sentimentanalysis", methods=["POST"])
def get_sentiment_analysis():
    keyword = request.args.get("keyword")
    start_date = request.args.get("start_date")
    df = get_articles_sentiments(keyword, start_date)
    return json.dumps(df.to_json())

@app.route("/api/generatesymbols", methods=["POST"])
def generate_symbols_():
    budget = request.args.get("budget")
    time_period = request.args.get("time_period")
    return generate_symbols(budget, time_period)

@app.route("/api/generateanalysis", methods=["POST"])
def generate_analysis_():
    date = request.args.get("date")
    open = request.args.get("open")
    high = request.args.get("high")
    low = request.args.get("low")
    volume = request.args.get("volume")
    predicted_close = request.args.get("predicted_close")
    predicted_return = request.args.get("predicted_return")
    mean_sentiment = request.args.get("mean_sentiment")
    analysis = generate_analysis(date, open, high, low, volume, predicted_close, predicted_return, mean_sentiment)
    return analysis

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
    pass