import alpaca_trade_api as tradeapi

from processing.alpaca.tasks import store_barset


class AlpacaEcho(object):
    """
    The alpaca echo simply allows the user to simultaneously
    fetch the results of their query and save an instance of
    that query.
    """

    def __init__(self):
        self.instance = tradeapi.REST()

    def get_barset(self, symbol, time_frame, **kwargs):
        barset = self.instance.get_barset(symbol, time_frame, **kwargs)
        store_barset.delay(barset.df.to_csv(), symbol, time_frame, **kwargs)
        return barset


if __name__ == '__main__':
    print('-| quick test')
    api = tradeapi.REST()

    # Get daily price data for AAPL over the last 5 trading days.
    barset = api.get_barset('AAPL', 'day', limit=5)
    aapl_bars = barset['AAPL']

    print(aapl_bars.df)
    print(aapl_bars.df['open'])
    print(aapl_bars.df.to_csv())

    # See how much AAPL moved in that time_frame.
    week_open = aapl_bars[0].o
    week_close = aapl_bars[-1].c
    percent_change = (week_close - week_open) / week_open * 100
    print('AAPL moved {}% over the last 5 days'.format(percent_change))
