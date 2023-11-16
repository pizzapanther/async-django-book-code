from .handler import WebSocketHandler


class WeatherSocket(WebSocketHandler):
  async def on_open(self):
    print("OPENED!!")

  async def on_message(self, data):
    print('MESSAGES', data)
    if data == 'close':
      await self.close()

  async def on_close(self):
    print("CLOSED")

  async def on_error(self, error):
    print(error)
