# Image for a Python 3 development environment
FROM quay.io/rofrano/nyu-devops-base:su25

# Set up the Python development environment
WORKDIR /app
COPY Pipfile Pipfile.lock ./
RUN sudo python -m pip install -U pip pipenv && \
    sudo pipenv install --system --dev

ENV PORT=8000
EXPOSE $PORT

# Enable color terminal for docker exec bash
ENV TERM=xterm-256color
