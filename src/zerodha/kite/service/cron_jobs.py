import time
import schedule
from zerodha.kite.service import algo
from zerodha.kite.utils import general_util

schedule.every(30).seconds.do(algo.algo_start)


def start_cron():
    while general_util.is_market_open():
        schedule.run_pending()
        time.sleep(1)
