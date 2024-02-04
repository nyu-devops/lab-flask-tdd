FROM python:3.11-slim

# Establish a working folder
WORKDIR /app

# Establish dependencies
COPY pyproject.toml poetry.lock ./
RUN python -m pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --without dev

# Copy source files last because they change the most
COPY wsgi.py .
COPY service ./service

# Become non-root user
RUN useradd -m -r service && \
    chown -R service:service /app
USER service

# Run the service on port 8080
EXPOSE 8080
CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:8080"]
