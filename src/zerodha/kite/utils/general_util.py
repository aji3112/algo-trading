import datetime

from zerodha.kite.utils import kite_constants, date_util

headers = {'authorization': kite_constants.authToken,
           'accept': 'application/json, text/plain, */*',
           # 'accept-encoding': 'gzip, deflate, br',
           'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,ta;q=0.6',
           'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
           'sec-ch-ua-mobile': '?0',
           'sec-fetch-dest': 'empty',
           'sec-fetch-mode': 'cors',
           'sec-fetch-site': 'same-origin',
           'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
           }


def is_market_open():
    if datetime.datetime.now().__le__(date_util.get_market_closing_time()) and datetime.datetime.now().__ge__(
            date_util.get_market_closing_time()):
        return 1
    else:
        return 0
