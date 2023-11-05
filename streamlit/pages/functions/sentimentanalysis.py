import pandas as pd
from newsapi import NewsApiClient
from datetime import timedelta, datetime
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from .settings import NEWS_API_KEY

sia = SentimentIntensityAnalyzer()

def get_articles_sentiments(keyword, start_date):
    news_api_client = NewsApiClient(api_key=NEWS_API_KEY)
    if (type(start_date)) == str:
        from_date = datetime.strptime(start_date, "%d-%b-%Y")
    else:
        from_date = start_date
    articles = news_api_client.get_everything(
        q=keyword,
        from_param=from_date.isoformat(),
        to=(from_date + timedelta(days=1)).isoformat(),
        language="en",
        sort_by="relevancy",
        page_size=100
    )
    article_content = ''
    # date_sentiments = {}
    date_sentiments_list = []
    seen = set()
    
    for article in articles["articles"]:
        if str(article["title"]) in seen:
            continue
        else:
            seen.add(str(article["title"]))
            article_content = str(article["title"]) + ". " + str(article["description"])
            sentiment = sia.polarity_scores(article_content)["compound"]
            # date_sentiments.setdefault(from_date, []).append(sentiment)
            date_sentiments_list.append((sentiment, article["url"], article["title"], article["description"]))
    return pd.DataFrame(date_sentiments_list, columns=["Sentiment", "URL", "Title", "Description"])