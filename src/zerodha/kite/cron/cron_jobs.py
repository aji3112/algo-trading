import time
import schedule

from zerodha.kite.algo import intraday_algo
from zerodha.kite.service import instruments
from zerodha.kite.utils import general_util

# schedule.every(1).minutes.do(intraday_algo.algo_start())
schedule.every(30).seconds.do(instruments.load_instrument_tokens)
schedule.every(30).minutes.do(instruments.calc_avg_volume)


# schedule.every().day.at(kite_constants.POSITION_CLOSE_TIME).do(position_book.close_all_open_position)


def start_cron():
    while general_util.is_market_open():
        schedule.run_pending()
        time.sleep(1)
