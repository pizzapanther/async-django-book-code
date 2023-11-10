import httpx
import pusher

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

  pusher_client = pusher.Pusher(
    app_id=settings.PUSHER_APP_ID,
    key=settings.PUSHER_KEY,
    secret=settings.PUSHER_SECRET,
    cluster=settings.PUSHER_CLUSTER,
    ssl=True
  )
  pusher_client.trigger(f"{lat},{lng}", "current-weather", data["current"])

  return data
