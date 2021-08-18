import datetime

def getMinuteMarketDataDate():
    todayDate = datetime.date.today()
    fromDate = todayDate + datetime.timedelta(days=-6)
    minuteMarketDataDate = {}
    minuteMarketDataDate['to'] = todayDate
    minuteMarketDataDate['from'] = fromDate
    return minuteMarketDataDate

def getMarketClosingTime():
    closingTime = datetime.datetime.now().time().replace(hour=15, minute=55, second=0, microsecond=0)
    return closingTime

def getMarketStartingTime():
    startingTime = datetime.datetime.now().time().replace(hour=9, minute=15, second=0, microsecond=0)
    return startingTime