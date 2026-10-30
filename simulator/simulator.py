"""Simulated industrial machine exposed over Modbus TCP.

Holding registers (function code 3):
  0 -> temperature x10 (652 = 65.2 C)
  1 -> motor speed in rpm
  2 -> fault flag (0 = OK, 1 = temperature above 75 C)
"""
import asyncio
import logging
import math
import random

from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusServerContext,
    ModbusSlaveContext,
)
from pymodbus.server import StartAsyncTcpServer

HOST = "0.0.0.0"
PORT = 5020
FAULT_TEMP_C = 75.0

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("simulator")


async def update_registers(context):
    """Update the three registers once per second."""
    t = 0
    while True:
        temperature = 65 + 12 * math.sin(t / 30) + random.uniform(-0.5, 0.5)
        rpm = int(1500 + 100 * math.sin(t / 10) + random.randint(-10, 10))
        fault = 1 if temperature > FAULT_TEMP_C else 0
        context[0].setValues(3, 0, [int(temperature * 10), rpm, fault])
        if t % 10 == 0:
            log.info("temp=%.1f C rpm=%d fault=%d", temperature, rpm, fault)
        t += 1
        await asyncio.sleep(1)


async def main():
    store = ModbusSlaveContext(
        hr=ModbusSequentialDataBlock(0, [0] * 10), zero_mode=True
    )
    context = ModbusServerContext(slaves=store, single=True)
    updater = asyncio.create_task(update_registers(context))
    log.info("Modbus TCP server listening on %s:%d", HOST, PORT)
    await StartAsyncTcpServer(context=context, address=(HOST, PORT))
    await updater


if __name__ == "__main__":
    asyncio.run(main())