import streamlit as st
import yfinance as yf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import requests
from datetime import timedelta
import matplotlib.pyplot as plt

symbol = ""
symbols = []

def analyze_symbol():
    if symbol != "":
        ticker = yf.Ticker(symbol)
        history = ticker.history(period="Max")
        stock_dataframe = pd.DataFrame(history)

        st.caption(symbol + "\'s Close (USD) History")
        st.line_chart(stock_dataframe, y="Close")

        x = stock_dataframe[['Open', 'High','Low', 'Volume']]
        y = stock_dataframe['Close']
        train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.2, shuffle=False)
        regression = LinearRegression()
        regression.fit(train_x, train_y)
        # the coefficient of determination R² 
        regression_confidence = regression.score(test_x, test_y)

        latest_stock_row = stock_dataframe.tail(1)
        date = latest_stock_row.index[0]
        x_predict = latest_stock_row[['Open', 'High','Low', 'Volume']]
        y_predict = regression.predict(x_predict)[0]
        open_predict = x_predict["Open"][0]
        return_predict = y_predict - open_predict

        st.header("Prediction")
        st.text("Linear Regression Confidence: " + str(regression_confidence))
        st.caption("Latest " + symbol + "\'s Stock Information")
        st.dataframe(x_predict)
        st.text(symbol + "\'s Predicted Close: " + str(y_predict))
        st.text(symbol + "\'s Predicted Return: " + str(return_predict))

        date = date - timedelta(days=1)
        date = date.strftime("%d-%b-%Y")
        sentiment_dataframe = pd.read_json(
            requests.post("http://localhost:5000/api/sentimentanalysis", params={
                "keyword": symbol,
                "start_date": date
            }).json())
        mean_sentiment = sentiment_dataframe["Sentiment"].mean()

        st.header("Sentiment Analysis")
        st.caption("News about " + symbol + " on " + date)
        st.dataframe(sentiment_dataframe[["Title", "Description", "Sentiment"]])

        st.caption(symbol + "\'s Sentiments Histogram")
        figure, axis = plt.subplots()
        axis.hist(sentiment_dataframe["Sentiment"])
        st.pyplot(figure)

        sentiment_level = (mean_sentiment + 1) * 2.5
        sentiment_category = ""
        if sentiment_level > 4:
            sentiment_category = "Very Positive"
        elif sentiment_level > 3:
            sentiment_category = "Positive"
        elif sentiment_level > 2:
            sentiment_category = "Neutral"
        elif sentiment_level > 1:
            sentiment_category = "Negative"
        else:
            sentiment_category = "Very Negative"
        st.text("The Average Sentiment is " + sentiment_category)
        st.text("Mean Sentiment Score: " + str(mean_sentiment))

        st.header("AI Generated Analysis")
        analysis = requests.post("http://localhost:5000/api/generateanalysis", params={
            "date": date,
            "open": open_predict,
            "high": x_predict["High"][0],
            "low": x_predict["Low"][0],
            "volume": x_predict["Volume"][0],
            "predicted_close": y_predict,
            "predicted_return": return_predict,
            "mean_sentiment": mean_sentiment
        }).content.decode("utf-8")
        st.markdown(analysis)

# The name of product
st.title("Single Stock Analysis")

st.header("Input")
symbol_input = st.text_input("Stock Symbol:")
if st.button("Analyze"):
    symbol = symbol_input

analyze_symbol()