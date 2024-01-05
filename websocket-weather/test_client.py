#!/usr/bin/env python3

import asyncio
import datetime
import json

import websockets


async def run_tests(location=[29.89,-98.25]):
  async for websocket in websockets.connect('ws://localhost:8000/ws'):
    try:
      data = json.dumps({"location": location})
      await websocket.send(data)

      async for message in websocket:
        print(datetime.datetime.now(), message)

    except websockets.ConnectionClosed:
      restart = input('Restart [y/n]? ')
      if restart.lower() == 'y':
        continue

      break

if __name__ == "__main__":
  asyncio.run(run_tests())
