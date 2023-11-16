from django import http
from django.conf import settings
from django.template.response import TemplateResponse

from djstorm.models import WeatherPoint


def locations(request):
  context = {
    'locations': settings.WEATHER_LOCATIONS,
  }
  return TemplateResponse(request, "djstorm-locations.html", context)
