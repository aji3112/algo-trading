import json
import logging
from types import SimpleNamespace

import requests
import pync

from zerodha.kite.domain.order_bo import OrderBo
from zerodha.kite.service import order
from zerodha.kite.utils import kite_constants, general_util


def get_position_book():
    position_book = {}
    try:
        position_book_response = requests.get(kite_constants.POSITION_BOOK_API, headers=general_util.headers)
        logging.info(position_book_response.text)
        json_data = json.loads(position_book_response.content, object_hook=lambda d: SimpleNamespace(**d))
        status = json_data.status
        if status == 'success':
            position_book['day'] = json_data.data.day
            position_book['net'] = json_data.data.net
        else:
            logging.error("Getting Position Book failed")
            pync.notify("Getting Position Book failed")
    except Exception as position_book_exception:
        logging.info(position_book_exception)

    return position_book


def check_open_position(symbol):
    open_quantity = 0
    try:
        position_book = get_position_book()
        net_positions = position_book['net']
        for position in net_positions:
            if position.tradingsymbol == symbol:
                logging.info("Open quantity for symbol {}".format(symbol))
                open_quantity = position.quantity
                break
    except Exception as check_open_position_exception:
        logging.info(check_open_position_exception)

    return open_quantity


def close_open_position(symbol):
    order_id = ''
    try:
        position_book = get_position_book()
        net_positions = position_book['net']
        for position in net_positions:
            if position.tradingsymbol == symbol:
                logging.info("Closing open position for symbol {}".format(symbol))
                trans_type = kite_constants.BUY if position.quantity > 0 else kite_constants.SELL
                exit_order_bo = OrderBo(position.tradingsymbol, position.quantity, 0, position.exchange, trans_type,
                                        kite_constants.MARKET,
                                        position.product)
                order_id = order.place_order(exit_order_bo)
                if not order_id:
                    logging.info("{} position not exited".format(symbol))
                else:
                    logging.info("{} position exited with orderId {}".format(symbol, order_id))
                break

    except Exception as close_open_position_exception:
        logging.info(close_open_position_exception)

    return order_id


def close_all_open_position():
    exit_count = 0
    try:
        position_book = get_position_book()
        net_positions = position_book['net']
        for position in net_positions:
            logging.info("Closing open position for symbol {}".format(position.tradingsymbol))
            exit_trans_type = kite_constants.SELL if position.quantity > 0 else kite_constants.BUY
            exit_order_bo = OrderBo(position.tradingsymbol, position.quantity, 0, position.exchange, exit_trans_type,
                                    kite_constants.MARKET,
                                    position.product)
            order_id = order.place_order(exit_order_bo)
            if not order_id:
                logging.info("{} position not exited".format(position.tradingsymbol))
            else:
                exit_count = exit_count + 1
                logging.info("{} position exited with orderId {}".format(position.tradingsymbol, order_id))

    except Exception as close_all_open_position_exception:
        logging.info(close_all_open_position_exception)

    return bool(exit_count)


def get_open_position_symbols():
    open_symbols = []
    try:
        position_book = get_position_book()
        net_positions = position_book['net']
        for position in net_positions:
            open_symbols.append(position.tradingsymbol)
        logging.info("Open position symbols fetched with size {}".format(len(open_symbols)))
    except Exception as close_all_open_position_exception:
        logging.info(close_all_open_position_exception)
