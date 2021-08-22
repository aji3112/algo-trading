from zerodha.kite.utils import kite_constants


class OrderBo:

    def __init__(self, symbol, quantity, price, exchange, transaction_type, order_type, product):
        self.user_id = kite_constants.USER_ID
        self.variety = 'regular'
        self.exchange = exchange
        self.tradingsymbol = symbol
        self.transaction_type = transaction_type
        self.order_type = order_type
        self.quantity = quantity
        self.price = price
        self.product = product
        self.validity = 'DAY'
        self.disclosed_quantity = 0
        self.trigger_price = 0
        self.squareoff = 0
        self.stoploss = 0
        self.trailing_stoploss = 0
