import httpx

from djstorm.models import WeatherPoint


def fetch_weather(lat, long):
  url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}"
  url += "&current=temperature_2m,apparent_temperature,is_day,weather_code,wind_speed_10m"

  response = httpx.get(url)
  data = response.json()

  wpoint = WeatherPoint(point=f"{lat},{long}", weather_data=data)
  wpoint.save()

  return data
