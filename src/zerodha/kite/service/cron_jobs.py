import time
import schedule
from zerodha.kite.utils import general_util


# schedule.every(30).seconds.do(algo.algo_start)
# schedule.every().day.at(kite_constants.POSITION_CLOSE_TIME).do(position_book.close_all_open_position)


def start_cron():
    while general_util.is_market_open():
        schedule.run_pending()
        time.sleep(1)
