import logging
import threading

from zerodha.kite.algo import intraday_algo
from zerodha.kite.config import config
from zerodha.kite.indicators import rsi, macd
from zerodha.kite.service import market_data, instruments

logging.info("############# Started sample ############")
config.intialize_config()

# todo
i = 0
threads = []

for symbol, token in instruments.scrips.items():
    i = i + 1
    if 200 < i <= 700:
        algoThread = threading.Thread(target=intraday_algo.intraday_algo, args=(symbol,))
        algoThread.start()
        threads.append(algoThread)

for thread in threads:
    thread.join()

exit()

logging.info("############# Completed sample ############")
