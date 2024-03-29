import pandas
import numpy


def get_rsi(ohlc: pandas.DataFrame, period: int = 14, round_rsi: bool = True):
    """ Implements the RSI indicator as defined by TradingView on March 15, 2021.
        The TradingView code is as follows:
        //@version=4
        study(title="Relative Strength Index", shorttitle="RSI", format=format.price, precision=2, resolution="")
        len = input(14, minval=1, title="Length")
        src = input(close, "Source", type = input.source)
        up = rma(max(change(src), 0), len)
        down = rma(-min(change(src), 0), len)
        rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))
        plot(rsi, "RSI", color=#8E1599)
        band1 = hline(70, "Upper Band", color=#C0C0C0)
        band0 = hline(30, "Lower Band", color=#C0C0C0)
        fill(band1, band0, color=#9915FF, transp=90, title="Background")
    :param ohlc:
    :param period:
    :param round_rsi:
    :return: an array with the RSI indicator values
    """

    delta = ohlc["close"].diff()

    up = delta.copy()
    up[up < 0] = 0
    up = pandas.Series.ewm(up, alpha=1 / period).mean()

    down = delta.copy()
    down[down > 0] = 0
    down *= -1
    down = pandas.Series.ewm(down, alpha=1 / period).mean()

    rsi = numpy.where(up == 0, 0, numpy.where(down == 0, 100, 100 - (100 / (1 + up / down))))

    ohlc['rsi'] = rsi

    return ohlc


def is_increasing_rsi(rsi_data_frame, time_interval):
    return all(rsi_data_frame['rsi'][i] <= rsi_data_frame['rsi'][i + 1] for i in
               range(len(rsi_data_frame['rsi']) - time_interval, len(rsi_data_frame['rsi']) - 1))


def is_decreasing_rsi(rsi_data_frame, time_interval):
    return all(rsi_data_frame['rsi'][i] >= rsi_data_frame['rsi'][i + 1] for i in
               range(len(rsi_data_frame['rsi']) - time_interval, len(rsi_data_frame['rsi']) - 1))
