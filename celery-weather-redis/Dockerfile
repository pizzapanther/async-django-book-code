FROM bitnami/minideb:bookworm

ARG userid
ARG groupid

RUN addgroup asyncdj --gid $groupid
RUN useradd -ms /bin/bash -u $userid -g $groupid asyncdj
RUN echo 'asyncdj ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

RUN mkdir -p /app
RUN chown -R asyncdj:asyncdj /app
WORKDIR /app

RUN install_packages python3-full pipx redis-tools

USER asyncdj
ENV HOME /home/asyncdj
RUN pipx ensurepath
RUN pipx install pdm
RUN pipx inject pdm pdm-django
