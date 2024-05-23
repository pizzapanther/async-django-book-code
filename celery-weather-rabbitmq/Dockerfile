FROM bitnami/minideb:bookworm

ARG userid
ARG groupid

COPY scripts/group_init.bsh /usr/local/bin
COPY scripts/user_init.bsh /usr/local/bin
COPY scripts/pipx_init.bsh /usr/local/bin

RUN group_init.bsh $groupid
RUN user_init.bsh $userid $groupid

RUN mkdir -p /app
RUN chown -R $userid:$groupid /app
WORKDIR /app

RUN install_packages python3-full pipx

USER $userid
RUN pipx_init.bsh $userid
