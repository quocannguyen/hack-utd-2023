import streamlit as st
import streamlit as st
from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv
from pages.functions.sentimentanalysis import get_articles_sentiments
from pages.functions.generativeai import generate_symbols, generate_analysis
import json

if not hasattr(st, 'already_started_server'):
    # Hack the fact that Python modules (like st) only load once to
    # keep track of whether this file already ran.
    st.already_started_server = True
    st.write('''
        The first time this script executes it will run forever because it's running a Flask server.

        Close this browser tab and open a new one to see StockItUp.
    ''')

    load_dotenv(".env")
    app = Flask(__name__)
    cors = CORS(app)
    app.config.from_pyfile("pages/functions/settings.py")

    app = Flask(__name__)

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

    app.run(threaded=True, port=5000)

# The name of product
st.title("StockItUp")

st.header("Get Ready to StockItUp and Fill Your Portfolio to the Brim!")
st.markdown("Harnessing the power of cutting-edge technology, StockItUp provides a comprehensive, AI-driven approach to algorithmic earnings forecasting and stock comparison. Our platform seamlessly integrates multiple advanced tools, including yFinance API, NewsAPI, Linear Regression, and OpenAI, to deliver unparalleled insights for investors, traders, and financial enthusiasts.")

st.header("AI-Powered Analysis and Prediction")
st.markdown("With our AI-powered predictive models leveraging the prowess of Linear Regression and OpenAI's sophisticated analysis, we offer robust predictions for a stock's close position, empowering you to make informed investment decisions.")

st.header("Comprehensive Stock Comparison")
st.markdown("Effortlessly compare stocks within your portfolio using our platform's sophisticated comparison algorithms, enabling you to identify trends, patterns, and potential opportunities for growth across various market sectors.")

st.header("Real-time Sentiment Analysis")
st.markdown("Stay ahead of the market sentiment with our real-time analysis of news data powered by NewsAPI. Gain deeper insights into market movements, trends, and potential influences on stock performance, allowing you to react swiftly to changing market dynamics.")

st.header("Intuitive and User-Friendly Interface")
st.markdown("Our user-friendly interface provides an intuitive and seamless experience, allowing you to navigate through complex financial data effortlessly. Access comprehensive analytics, charts, and reports with just a few clicks, enabling you to make informed decisions with confidence.")

st.header("Stay Informed, Make Educated Decisions")
st.markdown("Empower your investment strategies with data-driven insights and expert analysis. Join StockItUp today and unlock the power of AI-driven financial intelligence for more successful and informed trading decisions.")