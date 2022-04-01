# Image for a Python 3 development environment
FROM python:3.9-slim

# Add any tools that are needed beyond Python 3.9
RUN apt-get update && \
    apt-get install -y sudo vim git zip tree curl wget jq && \
    apt-get autoremove -y && \
    apt-get clean -y

# Add Java JRE-11 for SonarLint
RUN ARCH=x64; \
    if [ $(uname -m) == aarch64 ]; then ARCH=aarch64; fi && \
    mkdir -p /usr/lib/jvm && \
    wget -qO - https://github.com/AdoptOpenJDK/openjdk11-binaries/releases/download/jdk-11.0.9.1+1/OpenJDK11U-jre_${ARCH}_linux_hotspot_11.0.9.1_1.tar.gz | tar xzvf - -C /usr/lib/jvm && \
    export JAVA_HOME=/usr/lib/jvm/jdk-11.0.9.1+1-jre && \
    ln -s $JAVA_HOME/bin/java /usr/bin/java
ENV JAVA_HOME=/usr/lib/jvm/jdk-11.0.9.1+1-jre

# Create a user for development
ARG USERNAME=devops
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user with passwordless sudo privileges
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/bash \
    && usermod -aG sudo $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Added libraries for PostgreSQL
RUN apt-get install -y gcc libpq-dev

# Set up the Python development environment
WORKDIR /app
ENV PIPENV_VENV_IN_PROJECT "enabled"
RUN python -m pip install --upgrade pip wheel pipenv

ENV PORT 8000
EXPOSE $PORT

# Enable color terminal for docker exec bash
ENV TERM=xterm-256color

# Become a regular user
USER $USERNAME
