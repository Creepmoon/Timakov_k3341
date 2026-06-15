# Подзадача 1 — Docker

## Цель

Упаковать FastAPI-приложение (ЛР1), базу данных PostgreSQL и парсер (ЛР2) в Docker-контейнеры и управлять ими через Docker Compose.

## Сервис парсера

Парсер вынесен в отдельное FastAPI-приложение `parser_service`:

- `POST /parse?url=<URL>` — загрузка страницы, извлечение `<title>`, сохранение в таблицу `parsed_page`.

Пример ответа:

```json
{
  "message": "Parsing completed",
  "url": "https://example.com",
  "title": "Example Domain"
}
```

## Dockerfile для API

Файл `Dockerfile.api`:

- базовый образ `python:3.12-slim`;
- установка зависимостей из `requirements.txt`;
- копирование `app/`, `migrations/`, `alembic.ini`;
- entrypoint: ожидание БД, миграции Alembic, создание таблиц;
- команда: `uvicorn app.main:app --host 0.0.0.0 --port 8000`.

## Dockerfile для парсера

Файл `Dockerfile.parser`:

- тот же базовый образ Python;
- минимальный набор зависимостей (FastAPI, requests, BeautifulSoup, SQLModel);
- копирование `parser_service/`;
- команда: `uvicorn parser_service.main:app --host 0.0.0.0 --port 8001`.

## Docker Compose

Файл `docker-compose.yml` описывает оркестр:

| Сервис | Образ / сборка | Порт | Зависимости |
|--------|----------------|------|-------------|
| `db` | `postgres:16-alpine` | 5432 | — |
| `redis` | `redis:7-alpine` | 6379 | — |
| `parser` | `Dockerfile.parser` | 8001 | `db` |
| `api` | `Dockerfile.api` | 8000 | `db`, `parser`, `redis` |
| `celery_worker` | `Dockerfile.api` | — | `db`, `parser`, `redis` |

Healthcheck для PostgreSQL и Redis гарантирует, что зависимые сервисы стартуют после готовности инфраструктуры.

## Запуск

```bash
docker compose up --build
```

Проверка парсера напрямую:

```bash
curl -X POST "http://localhost:8001/parse?url=https://example.com"
```

## Зачем Docker

- **Консистентность** — одинаковое окружение на всех машинах.
- **Изоляция** — каждый компонент в своём контейнере.
- **Простое развёртывание** — одна команда `docker compose up`.
