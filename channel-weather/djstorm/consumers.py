import asyncio
import json

from django.conf import settings

import httpx

from channels.generic.websocket import AsyncJsonWebsocketConsumer, AsyncConsumer
from channels.layers import get_channel_layer

from djstorm.models import WeatherPoint


class WeatherConsumer(AsyncJsonWebsocketConsumer):
  async def connect(self):
    self.current_location = None
    await self.accept()

  async def disconnect(self, close_code):
    if self.current_location:
      await self.channel_layer.group_discard(self.current_location, self.channel_name)

  async def receive_json(self, data):
    if 'location' in data:
      if self.current_location:
        await self.channel_layer.group_discard(self.current_location, self.channel_name)

      self.current_location = "location_{}_{}".format(*data['location'])
      print('Joining:', self.current_location)
      await self.channel_layer.group_add(self.current_location, self.channel_name)

      point = "{},{}".format(*data['location'])
      wp = await WeatherPoint.objects.filter(point=point).afirst()
      if wp:
        await self.send_json({"weather": wp.weather_data['current']})

  async def receive_message(self, event):
    data = json.loads(event["message"])
    await self.send_json({"weather": data})


class WeatherFetchConsumer(AsyncConsumer):
  async def fetch_all(self, message):
    for location in settings.WEATHER_LOCATIONS:
      asyncio.create_task(self.fetch_weather(*location["location"]))

  async def fetch_weather(self, lat, lng):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lng}"
    url += "&current=temperature_2m,apparent_temperature,is_day,weather_code,wind_speed_10m"
    url += "&temperature_unit=fahrenheit&wind_speed_unit=mph"

    response = httpx.get(url)
    data = response.json()

    wpoint = WeatherPoint(point=f"{lat},{lng}", weather_data=data)
    await wpoint.asave()
    group_name = f"location_{lat}_{lng}"
    message = json.dumps(data['current'])
    channel_layer = get_channel_layer()
    print('Sending to', group_name, ':', data)
    await self.channel_layer.group_send(group_name, {"type": "receive.message", "message": message})
