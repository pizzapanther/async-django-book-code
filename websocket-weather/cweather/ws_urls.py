from django.urls import path, re_path

import djstorm.ws

urlpatterns = [
    path('ws', djstorm.ws.WeatherSocket),
]
