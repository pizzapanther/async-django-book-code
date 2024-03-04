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
  last_id = request.POST.get('last_id')

  while 1:
    wp = await WeatherPoint.objects.filter(point=f"{lat},{lng}").afirst()
    if last_id and wp and str(wp.id) == last_id:
      print('No New Data, Sleeping ...')
      await asyncio.sleep(30)
      continue

    print('Sending Data')
    return http.JsonResponse({'id': wp.id, 'weather': wp.weather_data['current']})
