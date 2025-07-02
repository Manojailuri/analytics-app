#!/usr/bin/env python
import os
import asyncio
import datetime
import random
import json
import pathlib
import ssl

from websockets.asyncio.server import serve

async def logg(websocket):
    while True:
        #message = datetime.datetime.utcnow().isoformat() + "Z"
        #await websocket.send(message)
        #await asyncio.sleep(random.random() * 2 + 1)
        event = await websocket.recv()
        msg = json.loads(event)
        if msg["type"] == "send":
        	file = open('specs.txt', 'a')
        	#file.write(msg["value"] + "Browser" + msg["Browser"] + "Device" + msg["Device"] + msg["OS"] +msg["engine"]+msg["architecture"]+ "\n")
        	file.write(str(msg) + "\n")
        	file.close()
        elif msg["type"] == "recv":
        	file = open('specs.txt', 'r')
        	for each in file:
        		await websocket.send(json.dumps({"value": each}))
        		print (each)
        	file.close()

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
localhost_pem = pathlib.Path(__file__).with_name("localhost.pem")
ssl_context.load_cert_chain(localhost_pem)
		
async def main():
	port = int(os.environ.get("PORT", "8001"))
	async with serve(logg, "", port):
		#await asyncio.get_running_loop().create_future()
		await asyncio.Future()
		
if __name__ == "__main__":
	asyncio.run(main())
