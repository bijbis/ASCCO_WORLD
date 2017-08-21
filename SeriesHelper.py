from influxdb import SeriesHelper


class RemoteMonitor(SeriesHelper):
    class Meta:
        client = None
        series_name = None
        fields = None
        tags = ['host', 'region']
        bulk_size = 1
        autocommit = True


class EnergyMonitor(SeriesHelper):
    class Meta:
        client = None
        series_name = None
        fields = None
        tags = ['host', 'region']
        bulk_size = 1
        autocommit = True
