FROM bitnami/minideb:bookworm

RUN mkdir /app
WORKDIR /app

RUN install_packages python3-full redis-tools

RUN curl -s https://bootstrap.pypa.io/get-pip.py | python3
RUN pip3 install pdm pdm-django toml
