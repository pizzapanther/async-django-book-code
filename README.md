# Async Patterns in Django Code

This repository contains full code examples for the book "Async Patterns in Django".

Purchase the book at: [www.asyncdjango.com](https://www.asyncdjango.com)

## How to Use This Code

Note, the included Docker Compose files work with Docker Engine or Docker Desktop CLI.

```bash
# Enter project directory
cd <project-directory>

# Build container
docker compose build --build-arg userid=$(id -u) --build-arg groupid=$(id -g)

# Enter container
docker compose run -p 8000:8000 django /bin/bash

# Install Django and other dependencies
pdm install
pdm manage migrate

# Run the fullstack
pdm run honcho start
```

## Included Projects

- **Celery Weather**<br>
**Description:** Implementation of Celery for fetching weather forecasts asynchronously. Implemented with a RabbitMQ broker and a Redis broker.<br>
**Project:** [celery-weather-rabbitmq](celery-weather-rabbitmq)<br>
**Project:** [celery-weather-redis](celery-weather-redis)<br><br>
- **Django Channel Weather**<br>
**Description:** Weather application using [Django Channels](https://channels.readthedocs.io/) and WebSockets.<br>
**Project:** [channel-weather](channel-weather)<br><br>
- **File Streamer**<br>
**Description:** Large file streaming application using asynchronous `StreamingHttpResponse`. Implements [HTTP Range Requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests).<br>
**Project:** [file-streamer](file-streamer)<br><br>
- **GraphQL Subscription Weather**<br>
**Description:** Weather application using [Graphene](https://graphene-python.org/) and GraphQL Subscriptions over a WebSocket.<br>
**Project:** [gql-weather](gql-weather)<br><br>
- **Long Polling Weather**<br>
**Description:** Weather application that uses [Long Polling](https://javascript.info/long-polling).<br>
**Project:** [long-weather](long-weather)<br><br>
- **Pusher Weather**<br>
**Description:** Weather application that uses the [Pusher Service](https://pusher.com/).<br>
**Project:** [pusher-weather](pusher-weather)<br><br>
- **SSE Weather**<br>
**Description:** Weather application that uses [Server Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events).<br>
**Project:** [sse-weather](sse-weather)<br><br>
- **WebSocket Weather**<br>
**Description:** Weather application using [WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API).<br>
**Project:** [websocket-weather](websocket-weather)
