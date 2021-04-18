import asyncio
from bleak import BleakClient
import sys
import time
import uuid
address = "64:69:4E:89:2B:C5"
write_characteristic = "0000FFE1-0000-1000-8000-00805f9b34fb"
async def connect():
    a = BleakClient(address)
    await a.connect()
    #await a.pair()
    try:
        await a.write_gatt_char(write_characteristic, b'p')
        print("started playing music")
        time.sleep(2)
        await a.write_gatt_char(write_characteristic, b'n')
        time.sleep(2)
        await a.write_gatt_char(write_characteristic, b'n')
        time.sleep(2)
        await a.write_gatt_char(write_characteristic, b'n')
        time.sleep(2)
        await a.write_gatt_char(write_characteristic, b'n')
        time.sleep(2)
        await a.write_gatt_char(write_characteristic, b's')
    except Exception as inst:
        print("Unexpected error:", inst)
        print("oh no")
    #finally:
    #    await a.unpair()
    await a.disconnect()
    print("stopped playing music")
asyncio.run(connect())
#connect()
