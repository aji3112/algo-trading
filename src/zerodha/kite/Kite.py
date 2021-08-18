from domain.orderBO import orderBO
import kiteConstants
import order
import sys
import numpy
numpy.set_printoptions(threshold=sys.maxsize)
import config

config.intializeConfig()

orderBO = orderBO()
orderBO.variety=kiteConstants.regular
orderBO.exchange=kiteConstants.nse
orderBO.tradingsymbol='HDFCBANK'
orderBO.transaction_type=kiteConstants.buy
orderBO.order_type=kiteConstants.market
orderBO.quantity=1
orderBO.price=1514.5
orderBO.product=kiteConstants.cnc
orderBO.validity=kiteConstants.day
orderBO.disclosed_quantity=0
orderBO.trigger_price=0
orderBO.squareoff=0
orderBO.stoploss=0
orderBO.trailing_stoploss=0

order.placeOrder(orderBO)

# marketDataDataFrame = marketData.getMinuteMarketData('HDFCBANK')
# rsiValues = rsi.rsi_tradingview(marketDataDataFrame)
# print(rsiValues)