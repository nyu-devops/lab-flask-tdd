# Image for a Python 3 development environment
FROM python:3.11-slim

# Add any tools that are needed beyond Python 3.11
RUN apt-get update && \
    apt-get install -y sudo vim make git zip tree curl wget jq procps net-tools && \
    apt-get autoremove -y && \
    apt-get clean -y

# Create a user for development
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user with passwordless sudo privileges
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/bash \
    && usermod -aG sudo $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && chown -R $USERNAME:$USERNAME /home/$USERNAME

# Set up the Python development environment
WORKDIR /app
COPY Pipfile Pipfile.lock ./
RUN python -m pip install -U pip pipenv && \
    pipenv install --system --dev

ENV PORT=8000
EXPOSE $PORT

# Enable color terminal for docker exec bash
ENV TERM=xterm-256color

# Become a regular user
USER $USERNAME
