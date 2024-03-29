import logging
import threading
import time

import pandas
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
market_data.get_market_data('HDFCBANK', kite_constants.FIVE_MINUTE, 25000, download=True)
exit()

logging.info("############# Completed sample ############")
