import datetime

from django import http
from django.utils import timezone

from djstorm.models import WeatherPoint
from djstorm.tasks import fetch_weather


def current_weather(request, lat, lng):
  wp = WeatherPoint.objects.filter(point=f"{lat},{lng}").first()
  old = timezone.now() - datetime.timedelta(minutes=15)

  if wp is None or wp.created <= old:
    print("Using Celery Task Data")
    async_result = fetch_weather.delay(lat, lng)
    data = async_result.get()

  else:
    print("Using Model Data")
    data = wp.weather_data

  data["current"]["app"] = "Celery Weather - Redis"
  return http.JsonResponse(data["current"])
