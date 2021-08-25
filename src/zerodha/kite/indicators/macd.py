import pandas


def get_macd(ohlc: pandas.DataFrame):
    # Get the 12-day EMA of the closing price
    period_12 = ohlc['close'].ewm(span=12, adjust=False, min_periods=12).mean()
    # Get the 26-day EMA of the closing price
    period_26 = ohlc['close'].ewm(span=26, adjust=False, min_periods=26).mean()
    # Subtract the 26-day EMA from the 12-Day EMA to get the MACD
    macd_diff = period_12 - period_26
    # Get the 9-Day EMA of the MACD for the Trigger line
    macd_signal = macd_diff.ewm(span=9, adjust=False, min_periods=9).mean()
    # Calculate the difference between the MACD - Trigger for the Convergence/Divergence value
    macd_histogram = macd_diff - macd_signal
    # Add all of our new values for the MACD to the dataframe
    ohlc['macd'] = ohlc.index.map(macd_diff)
    ohlc['macd_h'] = ohlc.index.map(macd_histogram)
    ohlc['macd_s'] = ohlc.index.map(macd_signal)

    # pandas.set_option("display.max_columns", None)
    # print(ohlc[['date','close','macd_s','macd','macd_h']])
    return ohlc


def is_increasing_histogram(macd_data_frame, time_interval):
    return all(macd_data_frame['macd_h'][i] <= macd_data_frame['macd_h'][i + 1] for i in
               range(len(macd_data_frame['macd_h']) - time_interval, len(macd_data_frame['macd_h']) - 1))


def is_decreasing_histogram(macd_data_frame, time_interval):
    return all(macd_data_frame['macd_h'][i] >= macd_data_frame['macd_h'][i + 1] for i in
               range(len(macd_data_frame['macd_h']) - time_interval, len(macd_data_frame['macd_h']) - 1))


def is_macd_crossed_signal_line(macd_data_frame):
    return macd_data_frame['macd_h'][len(macd_data_frame['macd_h']) - 1] >= 0
