from django.db import models
import uuid


class Providers:
    ALPACA = 'ALPACA'


class DataStages:
    ORIGINAL = 'ORIGINAL'
    CLEANED = 'CLEANED'
    DERIVED = 'DERIVED'


class DataStatus:
    INITIALIZED = 'INITIALIZED'
    INCOMPLETE = 'INCOMPLETE'
    COMPLETE = 'COMPLETE'
    FAILED_EXTERNALLY = 'FAILED_EXTERNALLY'
    FAILED_INTERNALLY = 'FAILED_INTERNALLY'


class Data(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    provider = models.TextField(null=True)
    provider_resource_path = models.TextField(null=True)
    file_format = models.TextField()
    stage = models.TextField()
    status = models.TextField(default=DataStatus.INITIALIZED)
    location = models.TextField()
    # a comma separated string of the search params in alphabetical order. Ex: a_time=100,b_time=200,ab=1,...
    search_kwargs = models.TextField(null=True)
    search_args = models.TextField(null=True)


class Symbol(models.Model):
    """
    A Symbol can have one to many EquityData objects pointing
    to it each at various stages.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    symbol = models.TextField()
    name = models.TextField()

    def get_price(self, start_date, end_date, precision='1d'):
        pass

    def get_volume(self, start_date, end_date, precision='1d'):
        pass


class EquityData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    exchange = models.TextField(null=True)
    category = models.TextField(null=True)  # price, volume, financial info, description, etc...
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    data = models.ForeignKey(Data, on_delete=models.CASCADE)
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)
