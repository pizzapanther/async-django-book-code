import asyncio

from django import http
from django.conf import settings
from django.template.response import TemplateResponse

from djstorm.models import WeatherPoint

from django_asse import SseStreamView, JsonEvent


def locations(request):
  context = {
    'locations': settings.WEATHER_LOCATIONS,
  }
  return TemplateResponse(request, "djstorm-locations.html", context)


class WeatherStream(SseStreamView):
  async def stream(self, request, lat, lng):
    last_update = None

    while 1:
      wp = await WeatherPoint.objects.filter(point=f"{lat},{lng}").afirst()

      if wp and wp.created != last_update:
        event = JsonEvent(event='weather', data=wp.weather_data['current'])
        last_update = wp.created
        print(f'Sending:\n{event}')
        yield event

      yield JsonEvent(event='ping', data=None)
      await asyncio.sleep(30)
