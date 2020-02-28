FROM python:3.7-slim

# Expose any ports the app is expecting in the environment
ENV PORT 5000
EXPOSE $PORT

# Create working folder and install dependencies
WORKDIR /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application contents
COPY app /app/app

ENV GUNICORN_BIND 0.0.0.0:$PORT
CMD ["gunicorn", "--log-level=info", "service:app"]
