# Image for a Python 3 development environment
FROM python:3.9-slim

# Add any tools that are needed beyond Python 3.9
RUN apt-get update \
    && apt-get install -y sudo git zip tree curl wget jq gcc libpq-dev \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Add Java JRE-8 for SonarLint
RUN mkdir -p /usr/lib/jvm \
    && wget -qO - https://github.com/AdoptOpenJDK/openjdk8-binaries/releases/download/jdk8u252-b09_openj9-0.20.0/OpenJDK8U-jre_x64_linux_openj9_8u252b09_openj9-0.20.0.tar.gz | tar xzvf - -C /usr/lib/jvm \
    && export JAVA_HOME=/usr/lib/jvm/jdk8u252-b09-jre \
    && ln -s $JAVA_HOME/bin/java /usr/bin/java
ENV JAVA_HOME=/usr/lib/jvm/jdk8u252-b09-jre

# Create a user for development
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/bash \
    && usermod -aG sudo $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Set up the development environment
WORKDIR /workspace
EXPOSE 5000

# Become a regular user
USER $USERNAME
