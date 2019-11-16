import uuid
import os

import alpaca_trade_api as tradeapi

from processing.alpaca.tasks import store_barset


class AlpacaEcho(object):
    """
    The alpaca echo simply allows the user to fetch
    and store equity data to a file
    """

    def __init__(self, temp_data_directory='alpaca_data'):
        self.instance = tradeapi.REST()
        self.current_working_directory = os.getcwd()
        self.temp_data_directory = os.path.join(self.current_working_directory, temp_data_directory)
        self._setup_temp_directory()

    def _setup_temp_directory(self):
        if not os.path.exists(self.temp_data_directory):
            os.mkdir(self.temp_data_directory)

    def write_data_frame_to_temp_file(self, data_frame):
        """
        Store a data frame to a file and return the file name.
        """
        file_name = f"{uuid.uuid4()}.csv"
        file_path = os.path.join(self.temp_data_directory, file_name)
        with open(file_path, 'w+') as data_file:
            data_file.write(data_frame.to_csv(index=True))
        return file_path

    def get_barset(self, symbol, time_frame, **kwargs):
        barset = self.instance.get_barset(symbol, time_frame, **kwargs)
        file_path = self.write_data_frame_to_temp_file(barset.df[symbol])
        store_barset.delay(file_path, symbol, time_frame, **kwargs)
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
