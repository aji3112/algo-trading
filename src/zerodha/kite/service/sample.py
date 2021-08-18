import logging

from zerodha.kite.service import cash

logging.info("Started sample")
cash.available_cash()