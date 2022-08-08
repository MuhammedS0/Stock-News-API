import requests
from twilio.rest import Client
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
API_KEY = "1QLQPLCST5KT9JNI"
ARTICLE_API_KEY = "e73a73d4bcff474c915b9f3bc3067285"
titles = []
descriptions = []
all_closed_prices = []
account_sid = "AC141cc63df051ac3ce413e912636d7fb8"
auth_token = "f35e95c3ba288dfa56fb651a1860b93a"

##STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
tesla_param = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": API_KEY
}

tesla_article_param = {
    "q": COMPANY_NAME,
    "language": "en",
    "apiKey": ARTICLE_API_KEY
}
# fetching article data
response_article = requests.get(url="https://newsapi.org/v2/everything", params=tesla_article_param)
response_article.raise_for_status()
data_article = response_article.json()
print(data_article)
the_articles = data_article["articles"]

for items in the_articles:
    titles.append(items["title"])
    descriptions.append(items["description"])

result = f"Headline: {titles[0]}\nBrief: {descriptions[0]}\n\nHeadline: {titles[1]}\nBrief: {descriptions[1]}\n\nHeadline: {titles[2]}\nBrief: {descriptions[2]}"

# fetching stock price data
response = requests.get(url="https://www.alphavantage.co/query", params=tesla_param)
response.raise_for_status()
data = response.json()
daily_tesla_data = data["Time Series (Daily)"]


#putting all of the closing tesla stock in a list
for item in daily_tesla_data:
    daily_data = daily_tesla_data[item]
    all_closed_prices.append(daily_data['4. close'])
    closed_prices = [float(i) for i in all_closed_prices]


#taking yesterdays and the days before's closing stocks to see the percent increase or decrease
print((closed_prices[0] - closed_prices[1]) / closed_prices[1] * 100)
if (closed_prices[0] - closed_prices[1]) / closed_prices[1] * 100 >= 5:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f"️TSLA: 🔺{(closed_prices[0] - closed_prices[1]) / closed_prices[1] * 100}\n{result}",
        from_="+12182824624",
        to="+14372466748"
    )
    print(message.status)
elif (closed_prices[0] - closed_prices[1]) / closed_prices[1] * 100 <= -5:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f"️TSLA: 🔻{abs((closed_prices[0] - closed_prices[1]) / closed_prices[1] * 100)}\n{result}",
        from_="+12182824624",
        to="+14372466748"
    )
## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

