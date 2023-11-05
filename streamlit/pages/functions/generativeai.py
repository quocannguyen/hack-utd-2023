import openai
from .settings import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_message(prompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message["content"]

def generate_symbols(budget, time_period):
    prompt = "Give me a comma delimited list of stock symbol, without a dot (\".\") in its symbol, affordable to the budget of $" + budget + " every " + time_period + ", to your knowledge, without anything else. Do not give me additional words."
    message = generate_message(prompt)
    symbols = message.split(',')
    symbols = [symbol.strip() for symbol in symbols]
    return symbols

def generate_analysis(date, open, high, low, volume, predicted_close, predicted_return, mean_sentiment):
    prompt = f"Based on the Date({date}), the Open({open}), the High({high}), the Low({low}), the Volume({volume}), the Predicted Close({predicted_close}), the Predicted Return({predicted_return}), and the Mean Sentiment Score({mean_sentiment}), please provide an Earnings Forecasting Analysis so that not only the stereo types of rich can use it, but also people everywhere of all abilities, without asking for additional data. Do not give out any disclaimer. Do not justify your answers. Do not give information not mentioned in the CONTEXT INFORMATION. Do not say it is not possible or requires additional data."
    message = generate_message(prompt)
    return message