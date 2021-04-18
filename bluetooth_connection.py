import asyncio
from bleak import BleakClient
import sys
import time

address = ("64:69:4E:89:2B:C5")
#address = ("DC5D07D7-38D1-4B52-94DA-4BDC300F5506") #uncomment for macos
write_characteristic = "0000FFE1-0000-1000-8000-00805f9b34fb"
async def connect():
    a = BleakClient(address)
    await a.connect()
    try:
        await a.write_gatt_char(write_characteristic, b'p')
        print("started playing music")
        time.sleep(2)
        #await a.write_gatt_char(write_characteristic, b's')
        #print("stopped playing music")
    except Exception as inst:
        print("Unexpected error:", inst)
        print("oh no")
    finally:
        await a.disconnect()
        
asyncio.run(connect())
