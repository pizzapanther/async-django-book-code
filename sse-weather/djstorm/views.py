import asyncio

from django import http
from django.conf import settings
from django.template.response import TemplateResponse

from djstorm.models import WeatherPoint


def locations(request):
  context = {
    'locations': settings.WEATHER_LOCATIONS,
  }
  return TemplateResponse(request, "djstorm-locations.html", context)

import json

from django.http import StreamingHttpResponse
from django.views import View


class SseStreamView(View):
  SSE_CONTENT_TYPE = 'text/event-stream'
  SSE_HEADERS = {
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
  }

  async def get(self, request, *args, **kwargs):
    return StreamingHttpResponse(
      (self._stream(request, *args, **kwargs)),
      content_type=self.SSE_CONTENT_TYPE,
      headers=self.SSE_HEADERS
    )

  def prepare_data(self, data):
    return data

  async def _stream(self, request, *args, **kwargs):
    async for event in self.stream(request, *args, **kwargs):
      if isinstance(event, dict):
        event['data'] = self.prepare_data(event['data'])

        if 'event' in event:
          event_string = "event: {event}\ndata: {data}\n\n".format(**event)

        else:
          event_string = "data: {}\n\n".format(event['data'])

      else:
        event = self.prepare_data(event)
        event_string = "data: {}\n\n".format(event)

      yield event_string


class JsonSseStreamView(SseStreamView):
  def prepare_data(self, data):
    return json.dumps(data)


class WeatherStream(JsonSseStreamView):
  async def stream(self, request, lat, lng):
    last_update = None

    while 1:
      wp = await WeatherPoint.objects.filter(point=f"{lat},{lng}").afirst()

      print(wp.created, last_update)
      if wp and wp.created != last_update:
        print(wp.weather_data['current'])
        yield {'event': 'weather', 'data': wp.weather_data['current']}

      await asyncio.sleep(60)
