# Async Patterns in Django Code

This repository contains full code examples for the book "Async Patterns in Django".

Purchase the book at: [www.asyncdjango.com](https://www.asyncdjango.com)

## How to Use This Code

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

- Celery Weather
Implementation of Celery for fetching weather forecasts asynchronously.
  - [celery-weather-rabbitmq](celery-weather-rabbitmq)
  - [celery-weather-redis](celery-weather-redis)
