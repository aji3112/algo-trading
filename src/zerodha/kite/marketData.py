import json
from types import SimpleNamespace
import requests
import kiteConstants
import scriptList
from util import util
import pync
import pandas
import dateUtil

def getMinuteMarketData(symbol):
    oi = 1
    fromDate = dateUtil.getMinuteMarketDataDate().get('from')
    toDate = dateUtil.getMinuteMarketDataDate().get('to')
    minute_market_data_api = kiteConstants.minute_market_data_api.replace('#token', scriptList.scrips.get(symbol))
    params = {'from': fromDate,
              'to': toDate,
              'oi': oi}
    utilities = util()
    try:
        minuteMarketDataResponse = requests.get(minute_market_data_api, headers=utilities.headers, params=params)
        jsonData = json.loads(minuteMarketDataResponse.content, object_hook=lambda d: SimpleNamespace(**d))
        marketData = jsonData.data.candles
        marketDataList = {'date':[], 'open':[], 'high': [], 'low': [], 'close': [], 'volume': [], 'oi' :[]}
        for data in marketData:
            marketDataList.get('date').append(data[0])
            marketDataList.get('open').append(data[1])
            marketDataList.get('high').append(data[2])
            marketDataList.get('low').append(data[3])
            marketDataList.get('close').append(data[4])
            marketDataList.get('volume').append(data[5])
            marketDataList.get('oi').append(data[6])

        marketDataFrame = pandas.DataFrame(marketDataList)
        print("Minute market data fetched for {} with size {}".format(symbol, marketDataFrame.size))

    except Exception as minuteMarketDataResponseException:
        print(minuteMarketDataResponseException)
        pync.notify(minuteMarketDataResponseException)

    return marketDataFrame
