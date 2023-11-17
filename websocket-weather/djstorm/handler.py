import asyncio
import datetime
import importlib
import json

from django.conf import settings
from django.core.handlers.asgi import ASGIRequest
from django.urls import resolve
from django.urls.exceptions import Resolver404
from django.utils import timezone

TASK_DUPLICATE_STARTED = "task-duplicate-started"
TASK_WS_CLOSED = "task-websocket-closed"


class WebSocketRequest(ASGIRequest):
  def __init__(self, scope, body_file):
    self.scope = scope
    self.scope['method'] = 'GET'
    super().__init__(self.scope, body_file)


class WebSocketHandler:
  LOOP_SLEEP_TIME = 0.3

  def __init__(self, request, receive, send):
    self.request = request
    self._receive = receive
    self._send = send

    self.connected = False
    self.closed = False
    self.tasks = {}

  async def sleep_loop(self, coroutine, cadence, *args, **kwargs):
    last_called = timezone.now()

    while 1:
      now = timezone.now()
      diff = (now - last_called).total_seconds()
      if diff >= cadence:
        await coroutine(*args, **kwargs)
        last_called = now

      await asyncio.sleep(self.LOOP_SLEEP_TIME)

  async def _ping(self):
    await self.send({'ping': timezone.now().isoformat()})

  async def ping(self):
    await self.sleep_loop(self._ping, 59)

  def start_ping(self):
    self.start_task('ping', self.ping)

  def start_task(self, task_id, coroutine, callback=None, args=None, kwargs=None):
    if args is None:
      args = []

    if kwargs is None:
      kwargs = {}

    if task_id in self.tasks and not self.tasks[task_id].done():
      self.tasks[task_id].cancel(msg=TASK_DUPLICATE_STARTED)

    task = asyncio.create_task(coroutine(*args, **kwargs))
    if callback:
      task.add_done_callback(callback)

    self.tasks[task_id] = task

  def cancel_tasks(self):
    for task_id, task in self.tasks.items():
      if not task.done():
        task.cancel(msg=TASK_WS_CLOSED)

  async def on_open(self):
    pass

  async def on_message(self, message):
    pass

  async def on_close(self):
    pass

  async def on_error(self, error):
    pass

  async def accept_connection(self):
    await self._send({'type': 'websocket.accept'})

  async def send(self, data):
    await self._send({'type': 'websocket.send', 'text': json.dumps(data)})

  async def process_message(self, msg):
    data = self.load_data(msg)
    await self.on_message(data)

  def load_data(self, msg):
    if 'text' in msg and msg['text']:
      return json.loads(msg['text'])

  async def close(self, code=1000):
    self.closed = True
    await self._send({'type': 'websocket.close', 'code': code})

  async def run_loop(self):
    try:
      while 1:
        msg = await self._receive()

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

    self.cancel_tasks()
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
