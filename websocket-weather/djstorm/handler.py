import importlib
import json

from django.conf import settings
from django.core.handlers.asgi import ASGIRequest
from django.urls import resolve
from django.urls.exceptions import Resolver404


class WebSocketRequest(ASGIRequest):
  def __init__(self, scope, body_file):
    self.scope = scope
    self.scope['method'] = 'GET'
    super().__init__(self.scope, body_file)


class WebSocketHandler:
  def __init__(self, request, receive, send):
    self.request = request
    self.receive = receive
    self.send = send

    self.connected = False
    self.closed = False

  async def on_open(self):
    pass

  async def on_message(self, message):
    pass

  async def on_close(self):
    pass

  async def on_error(self, error):
    pass

  async def accept_connection(self):
    await self.send({'type': 'websocket.accept'})

  async def process_message(self, msg):
    data = self.load_data(msg)
    await self.on_message(data)

  def load_data(self, msg):
    return json.loads(msg['text'])

  async def close(self, code=1000):
    self.closed = True
    await self.send({'type': 'websocket.close', 'code': code})

  async def run_loop(self):
    try:
      while 1:
        msg = await self.receive()

        if msg['type'] == 'websocket.connect':
          await self.accept_connection()
          self.connected = True
          await self.on_open()

        elif msg['type'] == 'websocket.disconnect':
          self.closed = True

        elif msg['type'] == 'websocket.receive':
          await self.process_message(msg)

        else:
          raise Exception('Unknown websocket event type: ' + event['type'])

        if self.closed:
          break

    except Exception as error:
      await self.on_error(error)
      raise

    await self.on_close()

def get_websocket_application():
  from django.core.asgi import get_asgi_application
  http_app = get_asgi_application()

  async def app(scope, receive, send):
    default_root_conf = settings.ROOT_URLCONF.replace('.urls', '.ws_urls')
    root_conf = getattr(settings, 'ROOT_WS_URLCONF', default_root_conf)

    if scope["type"] == "websocket":
      try:
        rmatch = resolve(scope['path'], urlconf=root_conf)

      except Resolver404:
        return await http_app(scope, receive, send)

      else:
        request = WebSocketRequest(scope, None)
        ws = rmatch.func(request, receive, send, *rmatch.args, **rmatch.kwargs)
        return await ws.run_loop()

    return await http_app(scope, receive, send)

  return app
