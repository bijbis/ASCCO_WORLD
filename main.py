from producer import ProducerThread
from consumer import ConsumerThread
from queue import Queue
from db import Influx
from SeriesHelper import RemoteMonitor, EnergyMonitor
import time


if __name__ == '__main__':
    energy_consumption = Queue()
    remote_monitor = Queue()
    database = Influx(database='influxDB', user='root', passcode='root', dbname='ascco_world',
                      port=8086, host='localhost')
    columns2 = [
        'ac_time',
        'total_energy'
    ]

    columns1 = [
        'ac_time',
        'current',
        'power',
        'power_factor',
        'voltage'
    ]

    EnergyMonitor.Meta.client = database.db
    EnergyMonitor.Meta.series_name = 'energy_consumption'
    EnergyMonitor.Meta.fields = columns2

    RemoteMonitor.Meta.client = database.db
    RemoteMonitor.Meta.series_name = 'remote_monitor'
    RemoteMonitor.Meta.fields = columns1

    p = ProducerThread(name='ModbusPull', que=[remote_monitor, energy_consumption])
    c = ConsumerThread(name='InfluxDBwriter', que=[remote_monitor, energy_consumption], db=database,
                       cols=[columns1, columns2])
    p.start()
    time.sleep(2)
    c.start()
    time.sleep(2)
