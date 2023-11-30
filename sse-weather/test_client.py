#!/usr/bin/env python3

from sseclient import SSEClient

def run():
  messages = SSEClient('http://localhost:8000/weather/52.13,13.14/')
  for msg in messages:
    print(msg)

if __name__ == "__main__":
  run()

