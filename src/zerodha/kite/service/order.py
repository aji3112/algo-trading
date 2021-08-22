import json
import logging
from types import SimpleNamespace

import pync
import requests
from zerodha.kite.utils import kite_constants
from zerodha.kite.utils import general_util


def place_order(order_bo):
    orderId = ''
    orderData = {'variety': order_bo.variety,
                 'exchange': order_bo.exchange,
                 'tradingsymbol': order_bo.tradingsymbol,
                 'transaction_type': order_bo.transaction_type,
                 'order_type': order_bo.order_type,
                 'quantity': order_bo.quantity,
                 'price': order_bo.price,
                 'product': order_bo.product,
                 'validity': order_bo.validity,
                 'disclosed_quantity': order_bo.disclosed_quantity,
                 'trigger_price': order_bo.trigger_price,
                 'squareoff': order_bo.squareoff,
                 'stoploss': order_bo.stoploss,
                 'trailing_stoploss': order_bo.trailing_stoploss,
                 'user_id': order_bo.user_id}

    try:
        place_order_response = requests.post(kite_constants.PLACE_ORDER_API, data=orderData,
                                             headers=general_util.headers)
        logging.info(place_order_response.text)
        json_data = json.loads(place_order_response.content, object_hook=lambda d: SimpleNamespace(**d))
        status = json_data.status
        if status == 'success':
            orderId = json_data.data.order_id
            message = 'order successful for symbol {} with transType {}'.format(order_bo.tradingsymbol,
                                                                                order_bo.transaction_type)
        else:
            message = 'order failed for symbol {} with transType {}'.format(order_bo.tradingsymbol,
                                                                            order_bo.transaction_type)
        pync.notify(message)
    except Exception as place_order_response_exception:
        logging.info(place_order_response_exception)

    return orderId
