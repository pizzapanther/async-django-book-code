"""
ASGI config for cweather project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cweather.settings')

from django_ws import get_websocket_application

application = get_websocket_application()

from luna_ws import add_ws_app

application = add_ws_app(application)
