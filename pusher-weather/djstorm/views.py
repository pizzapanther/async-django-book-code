from django import http
from django.conf import settings
from django.template.response import TemplateResponse

from djstorm.models import WeatherPoint


def locations(request):
  context = {
    'locations': settings.WEATHER_LOCATIONS,
  }
  return TemplateResponse(request, "djstorm-locations.html", context)


def current_weather(request, lat, lng):
  wp = WeatherPoint.objects.filter(point=f"{lat},{lng}").first()
  if wp is None:
    raise http.Http404

  context = {
    'pusher_key': settings.PUSHER_KEY,
    'pusher_cluster': settings.PUSHER_CLUSTER,
    'weather_point': wp,
    'channel': f"{lat},{lng}",
  }
  return TemplateResponse(request, "djstorm-dashboard.html", context)
