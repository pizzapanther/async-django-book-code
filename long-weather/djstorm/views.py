import asyncio

from django import http
from django.conf import settings
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt

from djstorm.models import WeatherPoint


def locations(request):
  context = {
    'locations': settings.WEATHER_LOCATIONS,
  }
  return TemplateResponse(request, "djstorm-locations.html", context)


@csrf_exempt
async def weather_stream(request, lat, lng):
  wait = request.POST.get('wait')

  if wait:
    print('Long Poll Started')
    await asyncio.sleep(30)

  wp = await WeatherPoint.objects.filter(point=f"{lat},{lng}").afirst()
  return http.JsonResponse(wp.weather_data['current'])
