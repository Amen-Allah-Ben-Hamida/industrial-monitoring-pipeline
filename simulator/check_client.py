"""Reads the 3 registers once, to check that the simulator answers."""
from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient("localhost", port=5020)
if not client.connect():
    raise SystemExit("Could not connect to the Modbus server")

result = client.read_holding_registers(0, 3, slave=1)
if result.isError():
    raise SystemExit(f"Modbus error: {result}")

temp10, rpm, fault = result.registers
print(f"temperature={temp10 / 10:.1f} C, rpm={rpm}, fault={fault}")
client.close()