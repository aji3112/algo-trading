import logging
import threading

from zerodha.kite.domain.order_bo import OrderBo
from zerodha.kite.indicators import rsi, macd
from zerodha.kite.service import market_data, order, instruments
from zerodha.kite.utils import kite_constants


def algo_start():
    threads = []
    for scrips in instruments.scrips:
        algoThread = threading.Thread(target=intraday_algo, args=(scrips,))
        algoThread.start()
        threads.append(algoThread)
    for thread in threads:
        thread.join()


def intraday_algo(symbol):
    logging.info("Intraday Algo started for symbol {} ".format(symbol))
    market_data_data_frame = market_data.get_minute_market_data(symbol)

    rsi_data_frame = rsi.get_rsi(market_data_data_frame)
    current_rsi = rsi_data_frame['rsi'][len(rsi_data_frame) - 1]
    logging.info("Current RSI for symbol {} : {}".format(symbol, current_rsi))
    is_increasing_rsi = rsi.is_increasing_rsi(rsi_data_frame, time_interval=2)
    logging.info("Is RSI increasing for symbol {} : {}".format(symbol, is_increasing_rsi))
    is_decreasing_rsi = rsi.is_decreasing_rsi(rsi_data_frame, time_interval=2)
    logging.info("Is RSI decreasing for symbol {} : {}".format(symbol, is_decreasing_rsi))

    macd_data_frame = macd.get_macd(market_data_data_frame)
    current_macd_h = macd_data_frame['macd_h'][len(macd_data_frame) - 1]
    logging.info("Current MACD_H for symbol {} : {}".format(symbol, current_macd_h))
    is_increasing_macd = macd.is_increasing_histogram(macd_data_frame, time_interval=2)
    logging.info("Is MACD_H increasing for symbol {} : {}".format(symbol, is_increasing_macd))
    is_decreasing_macd = macd.is_decreasing_histogram(macd_data_frame, time_interval=2)
    logging.info("Is MACD_H decreasing for symbol {} : {}".format(symbol, is_decreasing_macd))

    if current_rsi < 20:
        if is_increasing_rsi and is_increasing_macd:
            logging.info("Placing BUY order for symbol {}".format(symbol))
            buy_order_bo = OrderBo(is_increasing_macd, 1000, 0, kite_constants.NSE, kite_constants.BUY,
                                   kite_constants.MARKET,
                                   kite_constants.MIS)
            # order.place_order(buy_order_bo)
    elif current_rsi > 80:
        if is_decreasing_rsi and is_decreasing_macd:
            logging.info("Placing SELL order for symbol {}".format(symbol))
            sell_order_bo = OrderBo(symbol, 1000, 0, kite_constants.NSE, kite_constants.SELL, kite_constants.MARKET,
                                    kite_constants.MIS)
            # order.place_order(sell_order_bo)
    else:
        logging.info("No order placed for symbol {}".format(symbol))
