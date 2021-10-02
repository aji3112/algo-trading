import datetime

from zerodha.kite.utils import kite_constants


def default_market_data_start_date():
    return datetime.date(2001, 1, 1)


def get_market_closing_time():
    closingTime = datetime.datetime.now().replace(hour=23, minute=55, second=0, microsecond=0)
    return closingTime


def get_market_starting_time():
    startingTime = datetime.datetime.now().replace(hour=9, minute=15, second=0, microsecond=0)
    return startingTime
