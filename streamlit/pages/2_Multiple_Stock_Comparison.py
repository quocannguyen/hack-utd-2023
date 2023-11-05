import streamlit as st
import yfinance as yf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import requests
from datetime import timedelta

symbol = None
budget = None
time_period = None

if "symbol_dataframe" not in st.session_state:
    st.session_state["symbol_dataframe"] = pd.DataFrame(columns=["Symbol", "Open", "Return", "Sentiment"])
if "close_dataframe" not in st.session_state:
    st.session_state["close_dataframe"] = pd.DataFrame()
if "suggested_symbols" not in st.session_state:
    st.session_state["suggested_symbols"] = []

def analyze_symbol():
    if symbol:
        ticker = yf.Ticker(symbol)
        history = ticker.history(period="Max")
        stock_dataframe = pd.DataFrame(history)

        x = stock_dataframe[['Open', 'High','Low', 'Volume']]
        y = stock_dataframe['Close']
        train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.2, shuffle=False)
        regression = LinearRegression()
        regression.fit(train_x, train_y)

        latest_stock_row = stock_dataframe.tail(1)
        date = latest_stock_row.index[0]
        x_predict = latest_stock_row[['Open', 'High','Low', 'Volume']]
        y_predict = regression.predict(x_predict)[0]
        open_predict = x_predict["Open"][0]
        return_predict = y_predict - open_predict

        date = date - timedelta(days=1)
        date = date.strftime("%d-%b-%Y")
        sentiment_dataframe = pd.read_json(
            requests.post("http://localhost:5000/api/sentimentanalysis", params={
                "keyword": symbol,
                "start_date": date
            }).json())
        mean_sentiment = sentiment_dataframe["Sentiment"].mean()

        return open_predict, return_predict, mean_sentiment, stock_dataframe
    
def add_symbol_to_dataframe():
    if symbol:
        open_predict, return_predict, mean_sentiment, close_dataframe  = analyze_symbol()

        symbol_data = {
            "Symbol": symbol,
            "Open": open_predict,
            "Return": return_predict,
            "Sentiment": mean_sentiment
        }
        st.session_state["symbol_dataframe"] = pd.concat([st.session_state["symbol_dataframe"], pd.DataFrame([symbol_data])], ignore_index=True)

        close_dataframe[symbol] = close_dataframe["Close"]
        close_dataframe = close_dataframe.drop(["Open", "High", "Low", "Volume", "Dividends", "Stock Splits", "Close"], axis=1)
        session_close_dataframe = st.session_state["close_dataframe"]
        session_close_dataframe = pd.concat([session_close_dataframe, close_dataframe], axis=1)
        session_close_dataframe = session_close_dataframe[~session_close_dataframe.isnull().any(axis=1)]
        st.session_state["close_dataframe"] = session_close_dataframe
        
        st.caption("")
        st.dataframe(st.session_state["symbol_dataframe"])
        st.line_chart(st.session_state["close_dataframe"], y=st.session_state["symbol_dataframe"]["Symbol"])

def suggest_symbols():
    if budget and time_period:
        st.session_state["suggested_symbols"] = requests.post("http://localhost:5000/api/generatesymbols", params={
            "budget": budget,
            "time_period": time_period
        }).json()

# The name of product
st.title("Multiple Stock Comparison")

st.header("Input")
budget_input = st.text_input("Budget (in USD):")
time_period_selection = st.selectbox("Time Period:", [
    "Day",
    "Week",
    "2 weeks"
    "Month",
    "Quarter",
    "6 Months",
    "Year",
])
if st.button("Suggest"):
    budget = int(budget_input)
    time_period = time_period_selection
suggest_symbols()
st.text("Suggested Stock Symbols: " + str(st.session_state["suggested_symbols"]))

symbol_input = st.text_input("Stock Symbol:")
if st.button("Add"):
    symbol = symbol_input
add_symbol_to_dataframe()