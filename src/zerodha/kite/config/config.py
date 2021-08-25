import logging
import sys
from zerodha.kite.service import instruments
import numpy
import pandas


def intialize_config():
    instruments.load_instrument_tokens()
    numpy.set_printoptions(threshold=sys.maxsize)
    pandas.set_option("display.max_rows", None, "display.max_columns", None)
    logging.basicConfig(
        filename='/Users/ajith/Documents/kite-algo-trading/logs/kite-algo-trading-logs.log',
        format='%(asctime)s.%(msecs)03d %(levelname)s %(threadName)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
        force=True)
