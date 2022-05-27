FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

# library yang digunakan untuk menjalankan program game
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    libsdl-image1.2-dev \
    libsdl-mixer1.2-dev \
    libsdl-sound1.2-dev \
    vim \
    curl \
    make \
    sudo \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    python3-pip \
    tzdata \
    libssl-dev \
    openssl \
    zlib1g-dev \
    build-essential \
    checkinstall \
    libffi-dev \
    libsqlite3-dev \
    python3-pygame \
    libsdl1.2-dev \
    libsdl-ttf2.0-dev \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-gfx-dev \
    libsdl2-net-dev

# install pygame dan x11
RUN pip3 install pygame
RUN apt install -qqy x11-apps

ARG UID=1000
ARG GID=1000
ARG USER=docker

ARG PW=docker
RUN useradd -m ${USER} --uid=${UID} --shell /bin/bash && echo "${USER}:${PW}" | chpasswd \
    && adduser docker sudo

USER ${UID}:${GID}
WORKDIR /home/${USER}