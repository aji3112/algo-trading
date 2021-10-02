import datetime
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

pool = threading.BoundedSemaphore(5)


def get_market_data(symbol, type, period, download: bool = False):
    oi = 1
    json_data = ''
    market_data_frame = pandas.DataFrame
    from_date = datetime.datetime.today().date() - datetime.timedelta(days=period)
    if from_date < date_util.default_market_data_start_date():
        from_date = date_util.default_market_data_start_date()
    start_date = from_date
    to_date = datetime.datetime.today().date()
    time_range = general_util.get_market_data_date_range(type);
    try:
        delta = datetime.timedelta(days=time_range)
        while from_date <= to_date:
            market_data_api = kite_constants.MARKET_DATA_API.replace('#token', str(instruments.scrips.get(symbol))).replace('#timeframe', type)
            params = {'from': from_date, 'to': from_date + delta, 'oi': oi}
            market_data_response = api_call(market_data_api, general_util.headers, params)
            json_data = json.loads(market_data_response.content, object_hook=lambda d: SimpleNamespace(**d))
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
            logging.info("{} market data fetched for {} with size {} from {} to {}".format(type, symbol, market_data_frame.size, from_date, from_date + delta))
            from_date += delta

        logging.info("TOTAL market data size fetched for {} with size {} from {} to {}".format(symbol, market_data_frame.size, start_date, to_date))
        if download:
            file_name = kite_constants.HISTORICAL_MARKET_DATA_PATH.replace('*', symbol + '_' + type + '_' + start_date.strftime('%Y-%m-%d') + '_to_' + to_date.strftime('%Y-%m-%d'))
            market_data_frame.to_csv(file_name, index=False)
            logging.info("Market Data for {} with size {} downloaded to path {} ".format(symbol, market_data_frame.size, file_name))

    except Exception as market_data_response_exception:
        logging.error("Exception occurred while get_market_data for symbol {} with response {}".format(symbol, json_data, market_data_response_exception))
        pync.notify(market_data_response_exception)

    return market_data_frame


def api_call(market_data_api, headers, params):
    pool.acquire(blocking=True)
    market_data = requests.get(market_data_api, headers=headers, params=params)
    pool.release()
    return market_data
