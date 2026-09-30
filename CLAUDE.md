# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repo is a simple Flask application that exposes a REST API for managing pets. The code follows a classic MVC pattern: the `service/models.py` module contains the SQLAlchemy model, `service/routes.py` contains the Flask view functions, and `service/__init__.py` creates the Flask app. Common utilities for status codes, error handling, logging, and CLI commands live in `service/common`.

## Tech Stack

- Python 3.12 or greater
- Python Flask 3 framework for creating REST APIs
- SQLAlchemy Models for all database interactions
- PostgreSQL database for persistent storage
- PyUnit / unittest for all unit tests
- PyTest as a test runner only
- FactoryBoy for generating test data
- Honcho for running the application locally
- Gunicorn for running the application in production

Do not introduce:

- PyTest style unit tests, use unittest syntax instead
- Raw SQL statements, use SQLAlchemy models instead
unless explicitly requested.

## Code Architecture

- `service/__init__.py` – Flask app factory (`create_app`).
- `service/config.py` – Global configuration (database URI, secret key, logging level).
- `service/common/status.py` – HTTP status code constants.
- `service/common/error_handlers.py` – Flask error handlers for validation, 404, 415, 500, etc.
- `service/common/log_handlers.py` – Sets up gunicorn logging.
- `service/common/cli_commands.py` – CLI command `flask db-create` to rebuild tables.
- `service/models.py` – `Pet` SQLAlchemy model with CRUD methods and serialization.
- `service/routes.py` – REST endpoints (`/health`, `/`, `/pets`, `/pets/<id>`).
- `service/common` – Contains shared utilities.
- `tests/` – Test suite using `pytest`.
  - `tests/factories.py` – FactoryBoy factories for `Pet`.
  - `tests/pet_name_provider.py` – Faker provider for pet names.
  - `tests/test_routes.py` – Integration tests for API endpoints.
  - `tests/test_models.py` – Unit tests for the `Pet` model.
  - `tests/test_cli_commands.py` – Tests for the `flask db-create` command.

Rules:

- Keep all of the code that marshalls and unmarshalls web request in the controller
- Keep all of the business logic in the model
- The controller should not contain code that checks the input for validity. That should be delegated to the models `deserialize()` method.
- The control should never make an SQL query. That should be delegated to the models finder methods (e.g, `find_by_name()`).

## File Placement Rules

- Keep all of the controller code in `service/routes.py`
- Keep all of the model code in `service/models.py`
- Put shared helpers in `services/common`'
- Do not create a new abstraction for one-off usage
- Prefer editing existing components over creating near-duplicates
- Tests should be placed in the `tests` folder
- There should be one test file for each module under the service package
- The test files should be named `test_<service-module>.py`

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `DATABASE_URI` | `postgresql+psycopg://postgres:postgres@localhost:5432/postgres` | SQLAlchemy database connection |
| `SECRET_KEY` | `sup3r-s3cr3t` | Flask session secret |
| `FLASK_APP` | `wsgi:app` | Flask entry point |
| `PORT` | `8080` | Port for gunicorn |

## Coding Conventions

- Keep components focused and composable
- Extract repeated logic into helper functions
- Prefer descriptive variable names over abbreviations
- Use type hints for all variable definitions
- Use type hints on all method calls and return
- Use Google style docstring comments for all methods and functions
- Add additional comments only when intent is non-obvious
- Do not leave dead code or commented-out blocks

## Development Environment

The repo is designed to run in a Docker container or a VS Code Remote‑Containers environment. The `Dockerfile` installs dependencies via `pipenv`. The `Procfile` defines a single `web` process that runs `gunicorn`. The `runtime.txt` specifies the Python runtime for Heroku deployments.

## Common Commands

- **Build Docker image**
  ```bash
  docker build -t lab-flask-tdd .
  ```

- **Run the service locally**
  ```bash
  make run          # uses honcho to start gunicorn
  # or
  honcho start
  # or
  docker run -p 8080:8080 lab-flask-tdd
  ```

- **Initialize the database**
  ```bash
  make db-init      # runs `flask db-create`
  # or
  flask db-create
  ```

- **Install dependencies**
  ```bash
  make install      # pipenv install --system --dev
  ```

- **Create a virtualenv**
  ```bash
  make venv         # pipenv shell
  ```

- **Lint the code**
  ```bash
  make lint
  ```

- **Run all tests**
  ```bash
  make test
  # or
  pytest --pspec --cov=service --cov-fail-under=95
  ```

- **Run a single test**
  ```bash
  pytest tests/test_routes.py::TestPetService::test_get_pet
  # or
  pytest -k test_get_pet
  ```

## Testing and Quality

Tests are split into model tests, route tests, and CLI command tests. The `tests/factories.py` module uses FactoryBoy to generate realistic pet data.

The test suite uses `pytest` as a test runner with the `--pspec` flag for spec‑style output and `pytest-cov` for code coverage. The Makefile sets `RETRY_COUNT=1` during development to allow flaky tests to fail faster.

Before considering a task complete:

- run make test
- run make lint

A task is not complete unless all test cases pass and there are no linting errors or warnings.

Testing rules:

- if you write new code you should write a new test to test it
- maintain 95% code coverage overall
- all tests should be written using PyTest / Unittest syntax not PyTest
- use PyTest only as a test runner, never as a testing syntax
- do not add heavy test scaffolding for simple presentational sections
- ensure responsive behavior for Ul changes
- verify empty, loading, and error states where relevant

## Deployment

- **Docker**: `docker build` and `docker run`.
- **Heroku**: `runtime.txt` and `manifest.yml` configure the buildpack and environment.
- **Cloud Foundry**: `manifest.yml` defines the app and service binding.

## Additional Notes

- The service uses `retry` to wrap database initialization (`init_db`).
- The `service/models.py` module defines a `Gender` enum and uses `datetime.date` for birthdays.
- The `service/routes.py` module uses `abort` for error handling and `url_for` for generating resource URLs.
- The `service/common/status.py` module provides named HTTP status codes for readability.
- The `service/common/error_handlers.py` module registers handlers for `DataValidationError`, 404, 415, and 500 errors.
- The `service/common/log_handlers.py` module configures logging to match gunicorn’s format.
