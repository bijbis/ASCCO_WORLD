from pymodbus3.client.sync import ModbusTcpClient as ModbusClient
from pymodbus3.constants import Endian
from pymodbus3.payload import BinaryPayloadDecoder
import time
# import socket
import struct

NUMBER_OF_REGS = 4
client = ModbusClient('120.157.57.189', port=502)
# ip = socket.gethostbyname('paulharrison.hopto.org')
# client = ModbusClient(ip, port=502)
client.connect()

while True:
    try:
        rr2 = client.read_holding_registers(30513, NUMBER_OF_REGS, unit=2)
        decoder = BinaryPayloadDecoder.from_registers(rr2.registers, endian=Endian.Big)
        # raw = struct.pack('>HH', rr2.get_register(1), rr2.get_register(0))
        # val = struct.unpack('>f', raw)[0]
        # print(val)
        print(round(decoder.decode_64bit_uint(), 2))
        time.sleep(2)
    except struct.error:
        continue
