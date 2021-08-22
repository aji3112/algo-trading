import logging
import threading

from zerodha.kite.domain.order_bo import OrderBo
from zerodha.kite.indicators import rsi
from zerodha.kite.service import market_data, order, instruments
from zerodha.kite.utils import kite_constants


def algo_start():
    threads = []
    for scrips in instruments.scrips:
        algoThread = threading.Thread(target=rsi_algo, args=(scrips,))
        algoThread.start()
        threads.append(algoThread)
    for thread in threads:
        thread.join()


def rsi_algo(symbol):
    logging.info("Algo started with symbol {} ".format(symbol))
    market_data_data_frame = market_data.get_minute_market_data(symbol)
    rsi_values = rsi.get_rsi(market_data_data_frame)
    one_min_rsi = rsi_values[rsi_values.size - 1]
    logging.info("One minute RSI for symbol {} : {}".format(symbol, one_min_rsi))
    if one_min_rsi < 25:
        buy_order_bo = OrderBo(symbol, 1, 0, kite_constants.NSE, kite_constants.BUY, kite_constants.MARKET,
                               kite_constants.CNC)
        order.place_order(buy_order_bo)
    elif one_min_rsi > 80:
        sell_order_bo = OrderBo(symbol, 1, 0, kite_constants.NSE, kite_constants.SELL, kite_constants.MARKET,
                                kite_constants.CNC)
        order.place_order(sell_order_bo)
    else:
        logging.info("No order placed for symbol {}".format(symbol))


def exit_open_positions():
    logging.info("Algo started for checking and exiting open positions")
    try:
        #todo
        pass
    except Exception as exit_open_positions_exception:
        logging.error(exit_open_positions_exception)
