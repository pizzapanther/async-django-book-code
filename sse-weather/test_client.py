#!/usr/bin/env python3

import asyncio
import datetime

from aiohttp_sse_client2 import client as sse_client

async def run_tests(location='52.13,13.14'):
  url = f'http://localhost:8000/weather/{location}/'
  async with sse_client.EventSource(url) as event_source:
    async for event in event_source:
      print(datetime.datetime.now(), f"Event:{event.type}", event.data)


if __name__ == "__main__":
  asyncio.run(run_tests())

