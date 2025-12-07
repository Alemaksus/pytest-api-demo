# Framework Architecture

This document describes the API testing framework architecture in simple terms. It will help you understand how the framework is structured and how it works.

## 📁 Directory Structure

The framework is organized into several main modules:

### `client/` — API Client

This contains code for working with the API:

- **`api_base_client.py`** — base HTTP client. This is the main `BaseClient` class that can make requests (GET, POST, PUT, DELETE), log them, retry on errors (retry mechanism), and handle timeouts.
- **`exceptions.py`** — custom exceptions for handling API errors (`APIRequestException`, `APITimeoutException`, etc.).

**In simple terms:** This is the "middleman" between tests and the API. Instead of writing `requests.get()` in every test, we use `api_client.get()` — this is more convenient and reusable.

### `config/` — Configuration

Project settings:

- **`settings.py`** — `Settings` class that reads environment variables from the `.env` file (BASE_URL, tokens, timeouts, etc.).

**In simple terms:** This is where all settings are stored — where to send requests, which tokens to use, how long to wait for a response.

### `utils/` — Utilities

Helper functions used in tests:

- **`logging.py`** — centralized logging configuration. Contains `get_logger()` and `setup_logger()` functions for creating configured loggers in all framework modules.
- **`validators.py`** — functions for validating responses (checking status code, response time, JSON Schema).
- **`helpers.py`** — helper functions (extracting fields from JSON, checking status codes).
- **`data_generators.py`** — test data generators (creating random users, emails, etc.).
- **`models.py`** — Pydantic models for data validation (planned).

**In simple terms:** These are "tools" for tests — functions that help check responses, create test data, and log events.

### `tests/` — Tests

This is where all tests live:

- **`conftest.py`** — pytest fixtures. These are special functions that create an API client, get an authentication token, etc. They are automatically available in all tests.
- **`test_*.py`** — the tests themselves (CRUD tests, negative tests, performance tests, etc.).

**In simple terms:** These are the tests themselves and pytest settings that make tests more convenient.

### `data/` — Test Data

JSON files with schemas, data examples, etc.

## 🔄 Test Execution Flow

Let's break down how a test works from start to finish:

```
Test → Fixture → Client → Request → Response → Validator → Result
```

### Step 1: Test starts

```python
def test_create_user(auth_client):
    # Test begins
```

### Step 2: Fixture creates client

Pytest automatically calls the `auth_client` fixture from `conftest.py`:

- The `api_client` fixture creates a `BaseClient` object with settings from `config/settings.py`
- The `auth_token` fixture gets an authentication token
- The `auth_client` fixture combines them — creates a client with the token already set

**In simple terms:** A fixture is a "preparer". It prepares everything needed for the test (client, token) and passes it to the test.

### Step 3: Test makes request through client

```python
response = auth_client.post("/users", json=payload)
```

Inside `BaseClient.post()`:

- Full URL is built (base_url + path)
- Headers are added (including Authorization token)
- **Request is logged** (method, URL, parameters) via `utils/logging`
- HTTP request is sent via `requests.Session`
- **Response is logged** (status code, response time) via `utils/logging`
- If error — retries the request (retry mechanism)

**In simple terms:** The client handles all the "dirty work" — forms the URL, adds headers, logs every request and response (URL, status code, time), retries on errors.

### Step 4: Response received

`BaseClient` returns a `requests.Response` object with response data.

### Step 5: Response validation

The test checks the response:

```python
assert_status_code(response, 201)  # Status code check
validate_response_time(response, max_time_ms=1000)  # Time check
validate_pydantic_model(response.json(), UserModel)  # Structure check
```

**In simple terms:** Validators check that the response is correct — status code 201, response came quickly, data structure matches expected.

### Step 6: Result

If all checks pass — test is successful. If not — test fails with a clear error message.

## 📝 Where Things Are Stored

### Configuration

- **`.env`** — file with environment variables (BASE_URL, tokens, timeouts). This file is not committed to git.
- **`.env.example`** — example file with environment variables. Shows which variables are needed.
- **`config/settings.py`** — code that reads `.env` and provides settings via the `Settings` class.

**In simple terms:** Settings are stored in `.env`, and the code in `config/settings.py` reads them and makes them available to the entire framework.

### Test Data

- **`data/`** — folder with JSON files (schemas, data examples).
- **`utils/data_generators.py`** — code for generating test data on the fly (random emails, names, etc.).

**In simple terms:** Test data can be stored in files or generated programmatically.

## 🚀 How Tests Are Run

### Locally

1. **Activate virtual environment:**

   ```bash
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

2. **Environment setup:**
   - Copy `.env.example` to `.env`
   - Fill in real values (BASE_URL, tokens)

3. **Run tests:**

   ```bash
   pytest                    # All tests
   pytest -m smoke          # Only smoke tests
   pytest -v                # With verbose output
   pytest tests/test_crud_user.py  # Specific file
   ```

**In simple terms:** Activate environment, configure `.env`, run pytest.

### In CI (Continuous Integration)

Planned — adding GitHub Actions workflow (`.github/workflows/tests.yml`), which will:

1. Automatically run on every push to the repository
2. Install dependencies
3. Configure environment variables from GitHub secrets
4. Run all tests
5. Save reports as artifacts

**In simple terms:** CI automatically checks that all tests pass when someone adds new code.

## 🎯 Key Architecture Principles

1. **Separation of concerns:** Each module is responsible for its own task (client — for requests, validators — for checks, tests — for scenarios).

2. **Reusability:** Fixtures and utilities are used in all tests, not duplicated.

3. **Configurability:** All settings are in `.env`, easy to switch between environments (dev/staging/prod).

4. **Centralized logging:** All modules use a single logger from `utils/logging.py`, which ensures uniform log format and simplifies debugging.

5. **Simplicity:** Code is written to be easy to understand and extend.

## 📚 Interview Summary

If you need to briefly explain the architecture:

> "The framework consists of four main modules: `client/` — HTTP client for working with the API, `config/` — project settings, `utils/` — helper functions for validation and data generation, `tests/` — the tests themselves and pytest fixtures.
>
> The workflow is simple: test calls a fixture, which creates an API client, client makes a request, gets a response, test validates the response via utilities. Everything is logged and reused.
>
> Configuration is stored in the `.env` file, test data — in `data/` or generated programmatically. Tests run locally via pytest or automatically in CI on every commit."
