# SSE Weather Project

## Usage

```
# Build container
docker compose build --build-arg userid=$(id -u) --build-arg groupid=$(id -g)

# Enter container
docker compose run -P 8000:8000 django /bin/bash

# Install Django and other dependencies
pdm install
pdm manage migrate

# Download the Video File
aria2c -o files/bunny.m4v https://download.blender.org/peach/bigbuckbunny_movies/BigBuckBunny_640x360.m4v

# Run the fullstack
pdm run honcho start
```
