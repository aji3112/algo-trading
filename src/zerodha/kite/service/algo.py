import datetime
import logging
import threading
import time

from zerodha.kite.domain.orderbo import OrderBo
from zerodha.kite.indicators import rsi
from zerodha.kite.service import market_data, order
from zerodha.kite.utils import kite_constants, date_util, script_list


def algo_start():
    threads = []
    for scrips in script_list.scrips:
        algoThread = threading.Thread(target=rsi_algo, args=(scrips,))
        algoThread.start()
        threads.append(algoThread)
    for thread in threads:
        thread.join()
    time.sleep(30)


def rsi_algo(symbol):
    logging.info("Algo started with symbol {} ".format(symbol))
    market_data_data_frame = market_data.get_minute_market_data(symbol)
    rsi_values = rsi.rsi_tradingview(market_data_data_frame)
    one_min_rsi = rsi_values[rsi_values.size - 1]
    logging.info("One minute RSI for symbol {} : {}".format(symbol, one_min_rsi))
    if one_min_rsi < 25:
        buy_order_bo = OrderBo(symbol, 1, 0, kite_constants.nse, kite_constants.buy, kite_constants.market,
                               kite_constants.cnc)
        order.place_order(buy_order_bo)
    elif one_min_rsi > 80:
        sell_order_bo = OrderBo(symbol, 1, 0, kite_constants.nse, kite_constants.sell, kite_constants.market,
                                kite_constants.cnc)
        order.place_order(sell_order_bo)
    else:
        logging.info("No order placed for symbol {}".format(symbol))
