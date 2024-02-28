import requests
from twilio.rest import Client



STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API_KEY = 'KTFH9MFWB86QWU3D'
NEWS_API_KEY = '357fbee5367641678cb8987132a3bf08'
TWILIO_SID = "ACe1813fbfd042c2c67963494ba98cc891"
TWILIO_TOKEN = "14da9b0364dab12a8235c86520cb8d08"


STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "TSLA",
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT,params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]

#TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]

yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

#TODO 2. - Get the day before yesterday's closing stock price

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

#TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp

difference_stock_price = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
print(difference_stock_price)

#TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.

diff_percent = (difference_stock_price/ float(yesterday_closing_price)) * 100
print(diff_percent)
#TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").

if diff_percent > 0:
    news_params = {
        "apikey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

    three_articles = articles[:3]

    formatted_articles = [f"Headline: {article['title']}.\nBrief: {article['description']}" for article in three_articles]
    print(formatted_articles)

    client = Client(TWILIO_SID, TWILIO_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body= article,
            from_='+18589433357',
            to='+919156217510'
        )






#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

