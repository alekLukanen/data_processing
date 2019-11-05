from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.conf import settings


@shared_task(bind=True)
def store_barset(self, data, symbol, time_frame, **kwargs):
    print(f'store_barset: {symbol}, {time_frame}')
    print(f'DATA_DIR: {settings.DATA_DIR}')
    print(data)
