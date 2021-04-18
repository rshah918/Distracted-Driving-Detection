import asyncio
from bleak import BleakClient
import sys
import time
import uuid

write_characteristic = "0000FFE1-0000-1000-8000-00805f9b34fb"
address = "64:69:4E:89:2B:C5"

client  = BleakClient(address)

async def connect(client):
    try:
        await client.connect()
        #await client.pair()
        print("connected succesfully")
    except Exception as inst:
        print("Unexpected error:", inst)
        print("Did not connect to bluetooth module")

    #await asyncio.sleep(10)

async def speakerCommand(client, write_characteristic, command):
    #try:
    await client.write_gatt_char(write_characteristic, bytes(command, encoding='utf8'))
    if(command == 'p'):
      print("started playing music")
    else:
      print("stopped playing music")
    #except Exception as inst:
    #    print("Unexpected error:", inst)
    #    print("oh no")

async def disconnect(client):
    try:
        await client.disconnect()
        #await client.unpair()
    except Exception as inst:
        print("Unexpected error:", inst)


#client = BleakClient(address)

loop = asyncio.get_event_loop()
loop.run_until_complete(connect(client))
#asyncio.run(speakerCommand(client, write_characteristic, 'p'))
#asyncio.run(disconnect(client))
loop.run_until_complete(disconnect(client))
