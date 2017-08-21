from pymodbus3.client.sync import ModbusTcpClient as ModbusClient
import socket
import struct


class Modbus:
    def __init__(self, uri='localhost', port=502):
        self.host = socket.gethostbyname(uri)
        self.client = ModbusClient(self.host, port=port)
        self.client.connect()
        # // TODO implement a fallback
        # if not self.client:
        #     raise RuntimeError('Error establishing connection with uri {}'.format(uri))

    def _read(self, response, typ='Float32'):
        if typ == 'Float32':
            raw = struct.pack('>HH', response.get_register(1), response.get_register(0))
            return struct.unpack('>f', raw)[0]
        elif typ == 'Regular':
            return float(response.registers[0])

    def read(self, register, n, unit=1, typ='Float32'):
        response = self.client.read_holding_registers(register, n, unit=unit)
        return self._read(response, typ)

    def readN(self, registers, n, unit=1):
        # // TODO implement reading multiple registers
        pass
