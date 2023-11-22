from importlib import import_module

from asgiref.sync import sync_to_async

from django.contrib import auth
from django.conf import settings


class AuthAsyncMiddleware:
    def __init__(self, func):
        self.func = func

    async def __call__(self, ws):
        print('Pre Run Loop')

        if not hasattr(ws.request, 'user'):
            engine = import_module(settings.SESSION_ENGINE)
            SessionStore = engine.SessionStore
            session_key = ws.request.COOKIES.get(settings.SESSION_COOKIE_NAME)
            ws.request.session = SessionStore(session_key)
            ws.request.user = await sync_to_async(auth.get_user)(ws.request)

        print('USER:', ws.request.user)

        ret = await self.func(ws)

        print('POST Run Loop')

        return ret
