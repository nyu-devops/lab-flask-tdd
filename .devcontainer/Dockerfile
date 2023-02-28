FROM rofrano/nyu-devops-base:sp23

# Add Python package requiremnets to the dev environment
WORKDIR /app
COPY requirements.txt .
RUN sudo pip install -U pip wheel && \
    sudo pip install -r requirements.txt
