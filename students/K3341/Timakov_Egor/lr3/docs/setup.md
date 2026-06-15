# Установка и запуск

## Требования

- Docker Desktop 4.x+ (или Docker Engine + Docker Compose v2)
- Python 3.10+ — для локальной разработки без Docker
- Git

## Запуск через Docker Compose (рекомендуется)

```bash
cd students/K3341/Timakov_Egor/lr3
docker compose up --build
```

Остановка:

```bash
docker compose down
```

Полная очистка с удалением данных БД:

```bash
docker compose down -v
```

## Локальная разработка без Docker

### 1. Виртуальное окружение

```bash
cd lr3
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux / macOS
pip install -r requirements.txt
```

### 2. Переменные окружения

```bash
copy .env.example .env     # Windows
cp .env.example .env       # Linux / macOS
```

| Переменная | Описание | Значение по умолчанию |
|------------|----------|---------------------|
| `DB_URL` | PostgreSQL | `postgresql://postgres:postgres@localhost/collab_platform_db` |
| `PARSER_URL` | URL сервиса парсера | `http://localhost:8001` |
| `CELERY_BROKER_URL` | Брокер Celery | `redis://localhost:6379/0` |
| `CELERY_RESULT_BACKEND` | Хранилище результатов | `redis://localhost:6379/1` |

### 3. Запуск сервисов по отдельности

PostgreSQL и Redis можно поднять только из Compose:

```bash
docker compose up db redis -d
```

Запуск парсера:

```bash
uvicorn parser_service.main:app --host 0.0.0.0 --port 8001 --reload
```

Запуск API:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Запуск Celery worker:

```bash
celery -A app.celery_app worker --loglevel=info
```

## Документация MkDocs

```bash
pip install -r requirements.txt
mkdocs serve
```

Сайт: [http://127.0.0.1:8000](http://127.0.0.1:8000) (если порт свободен; иначе MkDocs выберет другой).

Статическая сборка:

```bash
mkdocs build
```

## Миграции БД

```bash
alembic upgrade head
```

Таблица `parsed_page` также создаётся автоматически при старте контейнера API и сервиса парсера.
