import logging
from zerodha.kite.config import config
from zerodha.kite.service import marketData, order
from zerodha.kite.indicators import rsi
from zerodha.kite.domain.orderBO import orderBO
import threading
import datetime
import time
from zerodha.kite.utils import dateUtil, kiteConstants, scriptList
from zerodha.kite.service import algo

config.intializeConfig()

threads = []
logging.info("Algo RSI and Order placing started")
while datetime.datetime.now().__le__(dateUtil.getMarketClosingTime()) and datetime.datetime.now().__ge__(dateUtil.getMarketClosingTime()):
    for scrips in scriptList.scrips:
        algoThread = threading.Thread(target=algo.algoStart, args=(scrips,))
        algoThread.start()
        threads.append(algoThread)

    for thread in threads:
        thread.join()

    time.sleep(30)

