"""
ASGI config for cweather project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from channels.security.websocket import AllowedHostsOriginValidator

from cweather.routing import websocket_urlpatterns
from djstorm.consumers import WeatherFetchConsumer, WeatherConsumer


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cweather.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
  "http": django_asgi_app,
  "websocket": AllowedHostsOriginValidator(URLRouter(websocket_urlpatterns)),
  "channel": ChannelNameRouter({"weather": WeatherFetchConsumer.as_asgi()}),
})
