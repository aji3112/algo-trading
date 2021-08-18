import datetime

def getMinuteMarketDataDate():
    todayDate = datetime.date.today()
    fromDate = todayDate + datetime.timedelta(days=-6)
    minuteMarketDataDate = {}
    minuteMarketDataDate['to'] = todayDate
    minuteMarketDataDate['from'] = fromDate
    return minuteMarketDataDate