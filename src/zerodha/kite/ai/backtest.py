import logging
import threading
import time
import pandas

from zerodha.kite.algo import intraday_algo
from zerodha.kite.config import config
from zerodha.kite.indicators import rsi, macd
from zerodha.kite.cron import cron_jobs
from zerodha.kite.service import market_data, instruments
import matplotlib.pyplot as plot

from zerodha.kite.utils import kite_constants, date_util

logging.info("############# Started sample ############")
config.intialize_config()

# todo
i = 0
market_data_frame = market_data.get_market_data("HDFCBANK", kite_constants.MINUTE, kite_constants.DEFAULT_MAX_MINUTE_MARKET_DATA_RANGE, download=False)
close_series = market_data_frame['close']
time_series = market_data_frame['date']
rsi_series = rsi.get_rsi(market_data_frame)['rsi']
plot.plot(time_series, close_series)
plot.plot(time_series, rsi_series)
plot.show()


exit()

logging.info("############# Completed sample ############")
