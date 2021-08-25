import json
import logging
import threading
from types import SimpleNamespace
import requests
from zerodha.kite.utils import general_util
import pync
import pandas
from zerodha.kite.service import instruments
from zerodha.kite.utils import date_util, kite_constants

pool = threading.BoundedSemaphore(6)


def get_minute_market_data(symbol):
    oi = 1
    json_data = ''
    market_data_frame = pandas.DataFrame
    from_date = date_util.get_minute_market_data_date().get('from')
    to_date = date_util.get_minute_market_data_date().get('to')
    minute_market_data_api = kite_constants.MINUTE_MARKET_DATA_API.replace('#token',
                                                                           str(instruments.scrips.get(symbol)))
    params = {'from': from_date, 'to': to_date, 'oi': oi}
    try:

        minute_market_data_response = api_call(minute_market_data_api, general_util.headers, params)
        json_data = json.loads(minute_market_data_response.content, object_hook=lambda d: SimpleNamespace(**d))
        market_data = json_data.data.candles
        market_data_list = {'date': [], 'open': [], 'high': [], 'low': [], 'close': [], 'volume': [], 'oi': []}
        for data in market_data:
            market_data_list.get('date').append(data[0])
            market_data_list.get('open').append(data[1])
            market_data_list.get('high').append(data[2])
            market_data_list.get('low').append(data[3])
            market_data_list.get('close').append(data[4])
            market_data_list.get('volume').append(data[5])
            market_data_list.get('oi').append(data[6])

        market_data_frame = pandas.DataFrame(market_data_list)
        logging.info("Minute market data fetched for {} with size {}".format(symbol, market_data_frame.size))

    except Exception as minute_market_data_response_exception:
        logging.error(
            "Exception occurred while get_minute_market_data for symbol {} with response {}".format(symbol, json_data,
                                                                                                    minute_market_data_response_exception))
        pync.notify(minute_market_data_response_exception)

    return market_data_frame


def api_call(market_data_api, headers, params):
    pool.acquire(blocking=True)
    market_data = requests.get(market_data_api, headers=headers, params=params)
    pool.release()
    return market_data
