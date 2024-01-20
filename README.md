# Async Patterns in Django Code

This repository contains full code examples for the book "Async Patterns in Django".

Purchase the book at: [www.asyncdjango.com](https://www.asyncdjango.com)

## How to Use This Code

Note, the included Docker Compose files work best with Docker Engine on the command line and not Docker Desktop. Docker Engine is freely installable on Linux, and Mac via Brew. On Windows it is recommended to use Docker Engine within WSL (Windows Subsystem for Linux) and your favorite Linux distro.

```bash
# Enter project directory
cd <project-directory>

# Build container
docker compose build --build-arg userid=$(id -u) --build-arg groupid=$(id -g)

# Enter container
docker compose run django /bin/bash

# Install Django and other dependencies
pdm install
pdm manage migrate

# Run the fullstack
pdm run honcho start
```

## Included Projects

- Celery Weather<br>
Implementation of Celery for fetching weather forecasts asynchronously. Implemented with a RabbitMQ broker and a Redis broker.
  - [celery-weather-rabbitmq](celery-weather-rabbitmq)
  - [celery-weather-redis](celery-weather-redis)
- Django Channel Weather - [channel-weather](channel-weather)<br>
Weather application using [Django Channels](https://channels.readthedocs.io/) and WebSockets.
- File Streamer - [file-streamer](file-streamer)<br>
Large file streaming application using asynchronous `StreamingHttpResponse`. Implements [HTTP Range Requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests).
- GraphQL Subscription Weather - [gql-weather](gql-weather)<br>
Weather application using [Graphene](https://graphene-python.org/) and GraphQL Subscriptions over a WebSocket.
- Long Polling Weather - [long-weather](long-weather)<br>
Weather application that uses [Long Polling](https://javascript.info/long-polling).
- SSE Weather - [sse-weather](sse-weather)<br>
Weather application that uses [Server Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events).
- WebSocket Weather - [websocket-weather](websocket-weather)<br>
Weather application using [WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API).
