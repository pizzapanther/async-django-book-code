from .handler import WebSocketHandler


class WeatherSocket(WebSocketHandler):
  async def on_open(self):
    self.current_location = None
    self.start_ping()

  async def on_message(self, data):
    if 'location' in data:
      self.current_location = "{},{}".format(*data['location'])
      self.start_task('send_weather', self.send_weather)

    else:
      print("Unknown message:", data)

  async def on_close(self):
    print("Connection Closed, Tasks Cancelled")

  async def on_error(self, error):
    print(error)

  async def _send_weather(self):
    #wp = WeatherPoint.objects.filter(point=f"{lat},{lng}").first()
    await self.send({"narf": 1})

  async def send_weather(self):
    await self.sleep_loop(self._send_weather, 5)
