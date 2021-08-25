import logging
from zerodha.kite.config import config
from zerodha.kite.cron import cron_jobs

config.intialize_config()

logging.info("Algo RSI and Order placing started")

cron_jobs.start_cron()
