import datetime


def get_minute_market_data_date():
    todayDate = datetime.date.today()
    fromDate = todayDate + datetime.timedelta(days=-6)
    minuteMarketDataDate = {'to': todayDate, 'from': fromDate}
    return minuteMarketDataDate


def get_market_closing_time():
    closingTime = datetime.datetime.now().replace(hour=15, minute=55, second=0, microsecond=0)
    return closingTime


def get_market_starting_time():
    startingTime = datetime.datetime.now().replace(hour=9, minute=15, second=0, microsecond=0)
    return startingTime
