# Pusher Weather Project

## Usage

Store your Pusher secrets and configuration in a `.env` in this directory.

```
PUSHER_APP_ID=123456
PUSHER_KEY=ahsjhfjksdhfkdjfklj
PUSHER_SECRET=kdfjkdjfkdjfkdjfkdjfkjdfkj
PUSHER_CLUSTER=us3
```

Then use the container like shown below.

```
# Build container
docker compose build --build-arg userid=$(id -u) --build-arg groupid=$(id -g)

# Enter container
docker compose run -P django /bin/bash

# Install Django and other dependencies
pdm install
pdm manage migrate

# Run the fullstack
pdm run honcho start
```
