import threading
import struct
import time
from modbus import Modbus
from datetime import datetime
from pymodbus3.exceptions import ModbusException
import sys
import os

class ProducerThread(threading.Thread):

    def __init__(self, group=None, target=None, name=None, que=None,
                 args=(), kwargs=None, verbose=None):
        super(self.__class__, self).__init__()
        self.target = target
        self.name = name
        self.q = que

    def run(self):
        modbus = Modbus.Modbus('ascoworldmodem.hopto.org')
        while True:
            item_remote_monitor = []
            item_energy_monitor = []
            try:
                now = datetime.now()
                ac_time = str(now.day) + '-' + str(now.month) + '-' + str(now.year) + '__' + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)
                current = float(modbus.read(13720, 1, typ='Regular')) * 0.01
                power = float(modbus.read(13696, 1, typ='Regular')) * 0.001
                power_factor = 1
                voltage = float(modbus.read(13716, 1, typ='Regular')) * 0.1
                item_remote_monitor.append(ac_time)
                item_remote_monitor.append(current)
                item_remote_monitor.append(power)
                item_remote_monitor.append(power_factor)
                item_remote_monitor.append(voltage)

                energy = float(modbus.read(7576, 1, typ='Regular'))
                item_energy_monitor.append(ac_time)
                item_energy_monitor.append(energy)
            except struct.error:
                print('Struct Error exception', file=sys.stderr)
                os._exit(1)
            except ModbusException:
                print('Modbus I/O exception', file=sys.stderr)
                os._exit(1)
            self.q[0].put(item_remote_monitor)
            self.q[1].put(item_energy_monitor)
            time.sleep(60)
