# API Testing Framework Demo

Lightweight and fast API testing framework for Python using pytest.

## 🎯 Project Description

This project is a template for creating an API testing framework in Python using pytest.

The framework provides basic structure and functionality for quick start with API testing:

- **Base API client** with session support, timeouts, and error handling
- **Pytest fixtures** for reuse in tests
- **Modular project structure** for easy extension
- **Environment variable configuration** for different environments

For more details on implemented features and development plans, see the [Framework Features](#-framework-features) section.

## ✨ Framework Features

### ✅ Implemented

#### 🔧 Base API Client

- **HTTP client based on requests**: Using `requests` library with session support
- **Session management**: Connection reuse via `requests.Session`
- **Timeouts**: Configurable timeouts for all requests
- **Centralized logging**: `utils/logging.py` module for uniform logging across the framework
- **Detailed request logging**: Automatic logging of URL, method, status code, and response time
- **Retry mechanism**: Automatic retries on errors (5xx, timeouts)
- **Custom exceptions**: Informative error handling (`APIRequestException`, `APITimeoutException`, etc.)
- **Type hints**: Type hints for better IDE support

#### 🧪 Tests and Fixtures

- **Pytest fixtures**: Centralized fixtures in `conftest.py` for reuse
- **Basic CRUD tests**: Examples of create, read, update, and delete resource tests
- **Test parametrization**: Using `@pytest.mark.parametrize` for negative tests

#### ⚙️ Configuration

- **config/ module**: Settings management via `config/settings.py`
- **Environment variables**: Support for different environments (dev/staging/prod/test) via `.env`
- **Configuration via .env**: Simple configuration through `.env.example` file

#### 🏗️ Project Structure

- **Modular architecture**: Separation into `client/`, `utils/`, `config/`, `tests/`
- **Reusable utilities**: Basic helpers and validators in `utils/` module

### 🧭 Planned

#### 📊 Extended Validation

- **Pydantic models**: Full Pydantic integration for type-safe data validation
- **JSON Schema validation**: Extended response structure validation via JSON Schema
- **Performance validation**: Automatic API response time checking

#### 📈 Reporting

- **Allure integration**: Detailed reports with steps, attachments, marker grouping
- **HTML reports**: Extended pytest HTML reports with additional information
- **Monitoring system integration**: Sending metrics and test results

#### 🎯 Data Generation

- **Faker integration**: Generating realistic test data using Faker library
- **UserDataGenerator**: Convenient classes for generating various types of test data

#### 🔄 CI/CD

- **GitHub Actions workflow**: Automatic test execution on multiple Python versions
- **Linting in CI**: Automatic code checking with ruff and mypy
- **Artifacts**: Saving reports and artifacts for analysis
- **Pre-commit hooks**: Automatic code checking before commit

#### 🧪 Extended Tests

- **Performance tests**: Automated checking of response time for various endpoints
- **Security tests**: Extended authorization checking, SQL injection protection, XSS, etc.
- **Database integration**: Utilities for working with databases in tests
- **External service mocking**: Integration with mocking libraries (responses, httpx)

#### 🐳 Infrastructure

- **Docker containerization**: Dockerfile and docker-compose for running tests in containers
- **Parallel execution**: Optimization of parallel test execution

## 📈 Benefits for Middle+ AQA Level

- **Professional structure**: Modular architecture, separation of concerns
- **Reliability**: Retry mechanism, error handling, data validation
- **Maintainability**: Documentation, type hints, logging
- **Scalability**: Easy to add new tests, flexible configuration
- **Code quality**: Linting, type hints, best practices

## 📋 Requirements

- Python 3.9+
- pip or poetry

## 🚀 Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd pytest-api-demo
```

2. Create a virtual environment:

```bash
python -m venv .venv
```

3. Activate the virtual environment:

```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

## 🏃 Running Tests

### Basic run of all tests

```bash
pytest
```

### Run with markers

```bash
# Only smoke tests
pytest -m smoke

# Skip slow tests
pytest -m "not slow"
```

### Run with Allure report

```bash
# Run with Allure results generation
pytest --alluredir=allure-results

# Open report in browser
allure serve allure-results
```

### Parallel execution

```bash
pytest -n auto
```

### Run with logging

```bash
pytest -v -s
```

## 📁 Project Structure

```
pytest-api-demo/
├── client/                      # API clients
│   ├── api_base_client.py       # Base HTTP client
│   ├── exceptions.py            # Custom exceptions
│   └── __init__.py              # Module export
├── tests/                       # Tests
│   ├── conftest.py              # Pytest configuration and fixtures
│   ├── test_crud_user.py        # CRUD tests
│   ├── test_create_user_negative.py  # Negative tests
│   ├── test_post_user.py        # User creation tests
│   ├── test_performance.py      # Performance tests
│   └── test_security.py         # Security tests
├── utils/                       # Utilities
│   ├── validators.py            # Response validators
│   ├── data_generators.py       # Test data generators
│   ├── helpers.py               # Helper functions
│   ├── models.py                # Pydantic models
│   └── __init__.py              # Module export
├── config/                      # Configuration
│   ├── settings.py              # Environment settings
│   └── __init__.py              # Module export
├── data/                        # Test data
│   └── endpoint_one.json        # JSON schemas
├── .env.example                 # Example environment variables file
├── requirements.txt             # Python dependencies
├── pytest.ini                   # Pytest configuration
├── pyproject.toml               # Project configuration
└── README.md                    # Documentation
```

## 🔧 Configuration

### Environment Setup

1. Copy `.env.example` file to `.env`:

   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and fill in real values:

   ```env
   BASE_URL=https://api.example.com
   ENV=dev
   LOG_LEVEL=INFO
   TIMEOUT=10
   ```

**Required variables:**

- `BASE_URL` - base API URL for testing
- `ENV` - environment (dev, staging, prod, test)

**Optional variables:**

- `TIMEOUT` - request timeout in seconds (default: 10)
- `LOG_LEVEL` - logging level (default: INFO)
- `AUTH_USERNAME` / `AUTH_PASSWORD` - authentication credentials
- `AUTH_TOKEN` - authentication token (if token is used directly)
- `RETRY_COUNT` - number of retry attempts on errors (default: 3)
- `RETRY_DELAY` - delay between attempts in seconds (default: 1.0)

### Environments

The project supports multiple environments:

- `dev` - development
- `staging` - testing
- `prod` - production
- `test` - test environment

Use the `ENV` variable to switch between environments.

## 📊 Reports

### Allure

After running tests with `--alluredir` flag:

```bash
allure serve allure-results
```

### Pytest HTML report

```bash
pytest --html=report.html --self-contained-html
```

## 🧪 Test Examples

### Simple test

```python
def test_get_user(api_client):
    response = api_client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
```

### Test with schema validation

```python
def test_create_user_success(auth_client):
    payload = {"email": "test@example.com", "role": "user"}
    response = auth_client.post("/users", json=payload)
    
    assert response.status_code == 201
    validate_json_schema(response.json(), user_schema)
```

## 🛠️ Development

### Linting

```bash
ruff check .
ruff format .
```

### Type checking

```bash
mypy .
```

### Logging

The framework uses centralized logging via the `utils/logging.py` module:

```python
from utils.logging import get_logger

logger = get_logger(__name__)
logger.info("Information message")
logger.debug("Debug message")
logger.warning("Warning")
logger.error("Error")
```

**What is logged automatically:**

- All HTTP requests (method, URL, parameters)
- All HTTP responses (status code, response time)
- Errors and retry attempts
- Test start and completion

**Logging level** is configured via the `LOG_LEVEL` environment variable in the `.env` file (DEBUG, INFO, WARNING, ERROR).

## 📝 Project Development

For a list of planned improvements and new features, see the [🧭 Planned](#-planned) section above.

If you would like to contribute to the framework development, create an issue or pull request with a description of the proposed changes.
