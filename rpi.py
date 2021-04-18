import asyncio
from bleak import BleakClient
import sys
import time
import uuid
address = ("64:69:4E:89:2B:C5")
write_characteristic = "0000FFE1-0000-1000-8000-00805f9b34fb"
#write_characteristic = "0000FFE1-0000-1000-8000-00805f9b34fb"
#0000FFE0
async def notification_handler(a1, a2):
  return
async def connect():
    a = BleakClient(address)
    #await a.pair()
    #await a.pair(1)
    await a.pair(2)
    #await a.pair(3)
    await a.connect()
    try:
      print("connected and paired")
      await a.start_notify(write_characteristic, notification_handler)
      x = await a.write_gatt_char(write_characteristic, data=b'p', response=True)
      await asyncio.sleep(0.5)
      x = await a.read_gatt_char(write_characteristic)
      await asyncio.sleep(0.5)
      print("started playing music")
      time.sleep(2)
      x = await a.write_gatt_char(write_characteristic, b'n', response=True)
      print("skipped")
      time.sleep(2)
      await a.write_gatt_char(write_characteristic, b'n')
      print("skipped")
      time.sleep(2)
      await a.write_gatt_char(write_characteristic, b'n')
      print("skipped")
      time.sleep(2)
      await a.write_gatt_char(write_characteristic, b'n')
      print("skipped")
      time.sleep(2)
      await a.write_gatt_char(write_characteristic, b's')
      print("stopped playing music")
    except Exception as inst:
      print("Unexpected error:", inst)
      print("oh no")
    finally:
      await a.disconnect()
      await a.unpair()
asyncio.run(connect())
