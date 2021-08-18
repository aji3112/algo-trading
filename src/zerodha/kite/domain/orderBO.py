from zerodha.kite.utils import kiteConstants


class orderBO:

    def __init__(self, symbol, quantity, price, exchange, transactionType, orderType, product):
        self.user_id = kiteConstants.userId
        self.variety = 'regular'
        self.exchange = exchange
        self.tradingsymbol = symbol
        self.transaction_type = transactionType
        self.order_type = orderType
        self.quantity = quantity
        self.price = price
        self.product = product
        self.validity = 'DAY'
        self.disclosed_quantity = 0
        self.trigger_price = 0
        self.squareoff = 0
        self.stoploss = 0
        self.trailing_stoploss = 0