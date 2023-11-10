from django.conf import settings
from django.template.response import TemplateResponse

from djstorm.models import WeatherPoint


def current_weather(request, lat, lng):
  wp = WeatherPoint.objects.filter(point=f"{lat},{lng}").first()
  context = {
    'pusher_key': settings.PUSHER_KEY,
    'pusher_cluster': settings.PUSHER_CLUSTER,
    'weather_point': wp,
    'channel': f"{lat},{lng}",
  }
  return TemplateResponse(request, "djstorm-dashboard.html", context)
