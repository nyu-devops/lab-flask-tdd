FROM python:3.8-slim

# establish working folder
WORKDIR /app

# add user and give ownership to workdir
RUN useradd -r -s /bin/bash worker
RUN chown -R worker:worker /app

USER worker

# set home & current env
ENV HOME /app
ENV PATH="/app/.local/bin:${PATH}"

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --user

# Copy the application contents
COPY config.py .
COPY service ./service

# Expose any ports the app is expecting in the environment
ENV PORT 5000
EXPOSE $PORT

ENV GUNICORN_BIND 0.0.0.0:$PORT
ENTRYPOINT ["gunicorn"]
CMD ["--log-level=info", "service:app"]
