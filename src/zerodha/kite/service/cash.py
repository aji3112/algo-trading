import json
import logging
from types import SimpleNamespace

import pync
import requests
from zerodha.kite.utils import general_util, kite_constants


def available_cash():
    cash_response = requests.get(kite_constants.cash_margin_api, headers=general_util.headers)
    cash_json = json.loads(cash_response.content, object_hook=lambda d: SimpleNamespace(**d))
    print(cash_response.content)
    status = cash_json.status
    net = 0.0
    try:
        if status == 'success':
            net = cash_json.data.equity.net
        else:
            net = 0.0
        logging.info("Available cash is {}".format(net))
    except Exception as cash_response_exception:
        pync.notify(cash_response_exception)
        logging.error(cash_response_exception)

    return net
