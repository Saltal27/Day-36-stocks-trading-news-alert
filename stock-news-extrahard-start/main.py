import requests
import datetime as dt

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

# ---------------------------- DETECTING STOCK BIG CHANGES ------------------------------- #
url = 'https://www.alphavantage.co/query'
parameters = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": "GB0YHQ6O8QMY7CVL",
}
connection = requests.get(url=url, params=parameters)
connection.raise_for_status()
data = connection.json()
time_series = data["Time Series (Daily)"]

today = dt.date.today()
yesterday = today - dt.timedelta(days=1)
the_day_before = today - dt.timedelta(days=2)

yesterday_close = float(time_series[str(yesterday)]["4. close"])
the_day_before_close = float(time_series[str(the_day_before)]["4. close"])

gap = abs(yesterday_close - the_day_before_close)
gap_percentage = (gap * 100) / the_day_before_close

if gap_percentage >= 5:
    print("Get News")

# ---------------------------- GETTING THE COMPANY'S LATEST NEWS ------------------------------- #
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

