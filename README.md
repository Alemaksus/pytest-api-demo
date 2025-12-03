# API Testing Framework Demo

Легкий и быстрый фреймворк для API-тестирования на Python с использованием pytest.

## 🎯 Описание проекта

Этот проект демонстрирует современный подход к автоматизации API-тестирования (Middle+ AQA). Фреймворк включает:

- **Базовый API-клиент** с поддержкой сессий, заголовков и обработкой ошибок
- **Структурированные тесты** с использованием pytest
- **Валидацию ответов** через JSON Schema и Pydantic models
- **Логирование** всех запросов и ответов
- **Генерацию тест-данных** с помощью Faker
- **Allure отчеты** для визуализации результатов
- **CI/CD интеграцию** для автоматического запуска тестов

## 📋 Требования

- Python 3.9+
- pip или poetry

## 🚀 Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd pytest-api-demo
```

2. Создайте виртуальное окружение:
```bash
python -m venv .venv
```

3. Активируйте виртуальное окружение:
```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

4. Установите зависимости:
```bash
pip install -r requirements.txt
```

## 🏃 Запуск тестов

### Базовый запуск всех тестов:
```bash
pytest
```

### Запуск с маркерами:
```bash
# Только smoke тесты
pytest -m smoke

# Пропустить slow тесты
pytest -m "not slow"
```

### Запуск с Allure отчетом:
```bash
# Запуск с генерацией Allure результатов
pytest --alluredir=allure-results

# Открыть отчет в браузере
allure serve allure-results
```

### Параллельный запуск:
```bash
pytest -n auto
```

### Запуск с логированием:
```bash
pytest -v -s
```

## 📁 Структура проекта

```
pytest-api-demo/
├── client/                 # API клиенты
│   ├── api_base_client.py  # Базовый HTTP клиент
│   └── api_client_fixtures.py  # Фикстуры для pytest
├── tests/                  # Тесты
│   ├── conftest.py         # Конфигурация pytest
│   ├── test_crud_user.py   # CRUD тесты
│   ├── test_create_user_negative.py  # Негативные тесты
│   └── test_post_user      # Тесты создания пользователя
├── utils/                  # Утилиты
│   ├── validators.py       # Валидаторы ответов
│   ├── data_generators.py  # Генераторы тест-данных
│   └── helpers.py          # Вспомогательные функции
├── config/                 # Конфигурация
│   └── settings.py         # Настройки окружений
├── data/                   # Тест-данные
│   └── endpoint_one.json   # JSON схемы
├── requirements.txt        # Зависимости Python
├── pytest.ini             # Конфигурация pytest
├── pyproject.toml          # Конфигурация проекта
└── README.md              # Документация
```

## 🔧 Конфигурация

### Переменные окружения

Создайте файл `.env` в корне проекта:

```env
BASE_URL=https://api.example.com
ENV=dev
LOG_LEVEL=INFO
TIMEOUT=10
```

### Окружения

Проект поддерживает несколько окружений:
- `dev` - разработка
- `staging` - тестирование
- `prod` - продакшн

Используйте переменную `ENV` для переключения окружений.

## 📊 Отчеты

### Allure

После запуска тестов с флагом `--alluredir`:

```bash
allure serve allure-results
```

### HTML отчет pytest

```bash
pytest --html=report.html --self-contained-html
```

## 🧪 Примеры тестов

### Простой тест:
```python
def test_get_user(api_client):
    response = api_client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
```

### Тест с валидацией схемы:
```python
def test_create_user_success(auth_client):
    payload = {"email": "test@example.com", "role": "user"}
    response = auth_client.post("/users", json=payload)
    
    assert response.status_code == 201
    validate_json_schema(response.json(), user_schema)
```

## 🛠️ Разработка

### Линтинг:
```bash
ruff check .
ruff format .
```

### Типизация:
```bash
mypy .
```

## 📝 Лицензия

MIT

## 👤 Автор

AQA Middle+ Demo Project



