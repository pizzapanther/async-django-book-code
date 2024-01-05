#!/usr/bin/env python3

import asyncio
import datetime

from gql import gql, Client
from gql.transport.websockets import WebsocketsTransport

QUERY_TEMPLATE = """
  subscription track {
    track_location(location: "{location}")
  }
"""

async def run_tests(location="29.89,-98.25"):
  transport = WebsocketsTransport(url='ws://localhost:8000/graphql')

  client = Client(transport=transport, fetch_schema_from_transport=False)
  query = QUERY_TEMPLATE.replace("{location}", location)
  query = gql(query)

  async for result in client.subscribe_async(query):
    print(datetime.datetime.now(), result)


if __name__ == "__main__":
  asyncio.run(run_tests())
