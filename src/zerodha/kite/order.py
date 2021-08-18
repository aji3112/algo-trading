import logging

import requests
import kiteConstants
from util import util


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
    except Exception as placeOrderResponseException:
        logging.info(placeOrderResponseException)
