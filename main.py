import requests
import datetime as dt
import smtplib

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

# ---------------------------- DETECTING STOCK BIG CHANGES ------------------------------- #
stocks_url = 'https://www.alphavantage.co/query'
stocks_parameters = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": "GB0YHQ6O8QMY7CVL",
}
stocks_response = requests.get(url=stocks_url, params=stocks_parameters)
stocks_response.raise_for_status()
stocks_data = stocks_response.json()
time_series = stocks_data["Time Series (Daily)"]

today = dt.date.today()
yesterday = today - dt.timedelta(days=1)
the_day_before = today - dt.timedelta(days=2)

yesterday_close = float(time_series[str(yesterday)]["4. close"])
the_day_before_close = float(time_series[str(the_day_before)]["4. close"])

gap = abs(yesterday_close - the_day_before_close)
gap_percentage = (gap * 100) / the_day_before_close

big_change = None
if gap_percentage >= 5:
    big_change = True
    if the_day_before_close > yesterday_close:
        emoji = "⬆️"
    else:
        emoji = "⬇️"


# ---------------------------- GETTING THE COMPANY'S LATEST NEWS ------------------------------- #
news_url = "https://newsapi.org/v2/top-headlines"
news_parameters = {
    "q": COMPANY_NAME,
    "apiKey": "afd3381f3c394b47997d3fd7bc2beadb",
}

news_response = requests.get(url=news_url, params=news_parameters)
news_response.raise_for_status()
news_data = news_response.json()
news_num = news_data["totalResults"]

if big_change:
    if news_num > 3:
        # get the first 3 pieces of news
        news_list = (news_data["articles"])[:3]
    elif 3 >= news_num > 0:
        # get all of them
        news_list = news_data["articles"]
    else:
        news_list = []

# ---------------------------- SENDING THE EMAIL ------------------------------- #
my_email = "pythontest32288@gmail.com"
my_password = "gsrfzucledwimgqp"

if big_change:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        if news_num == 0:
            connection.sendmail(
                from_addr=my_email,
                to_addrs="omarmobarak53@gmail.com",
                msg=f"Subject: Your {COMPANY_NAME} stocks are {emoji}{gap_percentage}%"
                    "\n\nRelative Headlines:\n"
                    "It seems that there aren't any breaking news regarding your stock."
            )
        else:
            for news_piece in news_list:
                connection.sendmail(
                    from_addr=my_email,
                    to_addrs="omarmobarak53@gmail.com",
                    msg=f"Subject: Your {COMPANY_NAME} stocks are {emoji}{gap_percentage}%"
                        "\n\nRelative Headlines:\n"
                        f"Headline: {news_piece['title']}\n"
                        f"Brief: {news_piece['description']}\n"
                        f"Url: {news_piece['url']}"
                )
