FROM bitnami/minideb:bookworm

RUN mkdir /app
WORKDIR /app

RUN install_packages python3-full pipx redis-tools

ENV HOME /root
RUN pipx ensurepath
RUN pipx install pdm
RUN pipx inject pdm pdm-django
