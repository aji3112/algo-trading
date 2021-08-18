import logging
import threading

from zerodha.kite.domain.orderBO import orderBO
from zerodha.kite.indicators import rsi
from zerodha.kite.service import marketData, order
from zerodha.kite.utils import kiteConstants


def algoStart(symbol):
    logging.info("Algo started with symbol {} ".format(symbol))
    marketDataDataFrame = marketData.getMinuteMarketData(symbol)
    rsiValues = rsi.rsi_tradingview(marketDataDataFrame)
    one_min_rsi = rsiValues[rsiValues.size - 1]
    logging.info("One minute RSI for symbol {} : {}".format(symbol, one_min_rsi))
    if one_min_rsi < 25:
        buyOrderBO = orderBO(symbol, 1, 0, kiteConstants.nse, kiteConstants.buy, kiteConstants.market, kiteConstants.cnc)
        order.placeOrder(buyOrderBO)
    elif one_min_rsi > 80:
        sellOrderBO = orderBO(symbol, 1, 0, kiteConstants.nse, kiteConstants.sell, kiteConstants.market, kiteConstants.cnc)
        order.placeOrder(sellOrderBO)
    else:
        logging.info("No order placed for symbol {}".format(symbol))