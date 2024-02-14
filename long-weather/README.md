# Long Poll Weather Project

## Usage

```
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
