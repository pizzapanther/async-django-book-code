import httpx

from celery import shared_task

from django.conf import settings

from djstorm.models import WeatherPoint


@shared_task
def fetch_all():
  for location in settings.WEATHER_LOCATIONS:
    fetch_weather.delay(*location["location"])


@shared_task
def fetch_weather(lat, lng):
  url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lng}"
  url += "&current=temperature_2m,apparent_temperature,is_day,weather_code,wind_speed_10m"
  url += "&temperature_unit=fahrenheit&wind_speed_unit=mph"

  response = httpx.get(url)
  data = response.json()

  wpoint = WeatherPoint(point=f"{lat},{lng}", weather_data=data)
  wpoint.save()

  return data
