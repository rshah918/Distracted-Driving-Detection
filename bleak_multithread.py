import asyncio
from bleak import BleakClient
import sys
import time
import _thread
import uuid
message = ''

async def connectionHandler():
    address = "64:69:4E:89:2B:C5"
    write_characteristic = "0000FFE1-0000-1000-8000-00805f9b34fb"
    a = BleakClient(address)
    await a.connect()
    global message
    while True:
        time.sleep(0.1)
        if not message == '':
            print(f'got a {message}')
            if message == 'd':
                await a.disconnect()
            else:
                await a.write_gatt_char(write_characteristic, bytes(message, encoding='utf8'))
            message = ''



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

_thread.start_new_thread(asyncio.run, (connectionHandler(),))
time.sleep(2)
message = 'p'
time.sleep(2)
message = 'n'
time.sleep(2)
message = 'n'
time.sleep(2)
message = 'n'
time.sleep(2)
message = 'n'
time.sleep(2)
message = 'n'
time.sleep(2)
message = 's'
time.sleep(2)
message = 'd'
time.sleep(2)

#asyncio.run(connect())
#connect()
