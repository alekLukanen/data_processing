from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.conf import settings

from processing.models import EquityData, Symbol, Data
import os
import json

ALPACA_DATA_DIR = os.path.join(os.getcwd(), 'data/alpaca')
if not os.path.exists(ALPACA_DATA_DIR):
    os.makedirs(ALPACA_DATA_DIR)

@shared_task(bind=True)
def store_barset(self, file_path, symbol, time_frame, **kwargs):
    print(f'file_path: {file_path}')
    print(f'symbol: {symbol}')
    print(f'time_frame: {time_frame}')
    print(f'DATA_DIR: {settings.DATA_DIR}')
    print(f'os.getcwd(): {os.getcwd()}')

    perm_file_name = os.path.basename(file_path)
    perm_file_path = os.path.join(ALPACA_DATA_DIR, perm_file_name)

    # move the file to the permanent directory
    os.rename(file_path, perm_file_path)

    search_kwargs = {
        "symbol": symbol,
        "time_frame": time_frame,
    }
    data = Data.objects.create(
        provider=kwargs.get('provider'),
        provider_resource_path=kwargs.get('provider_resource_path'),
        file_format='csv',
        file_location=perm_file_path,
        search_kwargs=json.dumps(search_kwargs)
    )

    symbol, _ = Symbol.objects.get_or_create(
        name=symbol.upper()
    )
    equity_data = EquityData.objects.create(symbol=symbol, data=data)
    print(f'equity_data: {equity_data}')


