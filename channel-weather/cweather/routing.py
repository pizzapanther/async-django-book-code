from django.urls import path

import djstorm.consumers


websocket_urlpatterns = [
  path(r"ws", djstorm.consumers.WeatherConsumer.as_asgi()),
]
