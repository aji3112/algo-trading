import logging
import pync
import requests
import pandas

from zerodha.kite.utils import kite_constants, general_util

global scrips


def download_instrument_tokens_csv():
    try:
        instrument_token_response = requests.get(kite_constants.INSTRUMENT_TOKEN, headers=general_util.headers)
        csv_file = open(kite_constants.INSTRUMENT_TOKEN_CSV_PATH, 'w+b')
        csv_file.write(instrument_token_response.content)
        csv_file.close()
    except Exception as instrument_token_exception:
        logging.error(instrument_token_exception)
        pync.notify(instrument_token_exception)


def read_instrument_tokens():
    stock_dictionary = pandas.DataFrame
    try:
        csv_data = pandas.read_csv(kite_constants.INSTRUMENT_TOKEN_CSV_PATH)
        # filtered_data = csv_data[csv_data.tick_size.isin([0.05]) & csv_data.exchange.isin(['NSE']) & csv_data.instrument_type.isin(['EQ'])]
        tick_size_criterion = csv_data['tick_size'].map(lambda x: x == 0.05)
        exchange_criterion = csv_data['exchange'].map(lambda x: x == 'NSE')
        lot_size_criterion = csv_data['lot_size'].map(lambda x: x == 1)
        instrument_type_criterion = csv_data['instrument_type'].map(lambda x: x == 'EQ')
        trading_symbol_criterion = csv_data['tradingsymbol'].map(lambda x: True if '-' not in x else False)
        filtered_data = \
        csv_data[tick_size_criterion][exchange_criterion][instrument_type_criterion][lot_size_criterion][
            trading_symbol_criterion][['tradingsymbol', 'instrument_token']]
        stock_dictionary = pandas.Series(filtered_data.instrument_token.values,
                                         index=filtered_data.tradingsymbol).to_dict()
        logging.info('EQ Series stocks fetched with size'.format(len(stock_dictionary)))
    except Exception as load_instrument_tokens_exception:
        logging.error(load_instrument_tokens_exception)
        pync.notify(load_instrument_tokens_exception)
    return stock_dictionary


def load_instrument_tokens():
    global scrips
    logging.info("Loading Instrument Tokens")
    download_instrument_tokens_csv()
    scrips = read_instrument_tokens()
    logging.info("Instrument Tokens loaded with size".format(len(scrips)))
