from django_ws import WebSocketHandler
from djstorm.models import WeatherPoint


class WeatherSocket(WebSocketHandler):
  async def on_open(self):
    self.current_location = None
    self.start_ping()

  async def on_message(self, data):
    if 'location' in data:
      if 'send_weather' in self.tasks:
        self.tasks['send_weather'].cancel()

      self.current_location = "{},{}".format(*data['location'])
      self.start_task('send_weather', self.send_weather)

    else:
      print("Unknown message:", data)

  async def on_close(self):
    print("Connection Closed, Tasks Cancelled")

  async def on_error(self, error):
    print("ERROR", error)

  async def _send_weather(self):
    if self.current_location:
      wp = await WeatherPoint.objects.filter(point=self.current_location).afirst()
      if wp:
        print("SENDING", wp.weather_data['current'])
        await self.send({"weather": wp.weather_data['current']})

  async def send_weather(self):
    await self._send_weather()
    await self.sleep_loop(self._send_weather, 60 * 3)
