import json
import logging
from types import SimpleNamespace

import pync
import requests
from zerodha.kite.utils import kiteConstants
from zerodha.kite.utils.generalUtil import util


def placeOrder(orderBO):
    orderData = {'variety': orderBO.variety,
                 'exchange': orderBO.exchange,
                 'tradingsymbol': orderBO.tradingsymbol,
                 'transaction_type': orderBO.transaction_type,
                 'order_type': orderBO.order_type,
                 'quantity': orderBO.quantity,
                 'price': orderBO.price,
                 'product': orderBO.product,
                 'validity': orderBO.validity,
                 'disclosed_quantity': orderBO.disclosed_quantity,
                 'trigger_price': orderBO.trigger_price,
                 'squareoff': orderBO.squareoff,
                 'stoploss': orderBO.stoploss,
                 'trailing_stoploss': orderBO.trailing_stoploss,
                 'user_id': orderBO.user_id}

    utilities = util()
    try:
        placeOrderResponse = requests.post(kiteConstants.place_order_api, data=orderData, headers=utilities.headers)
        logging.info(placeOrderResponse.text)
        jsonData = json.loads(placeOrderResponse.content, object_hook=lambda d: SimpleNamespace(**d))
        status = jsonData.status
        orderId = ''
        if status == 'success':
            orderId = jsonData.data.order_id
            message = 'order successful for symbol {} with transType {}'.format(orderBO.tradingsymbol, orderBO.transaction_type)
        else:
            message = 'order failed for symbol {} with transType {}'.format(orderBO.tradingsymbol, orderBO.transaction_type)
        pync.notify(message)
    except Exception as placeOrderResponseException:
        logging.info(placeOrderResponseException)

    return orderId