# Лабораторная работа 3

**Тема:** контейнеризация приложений с Docker, интеграция парсера через HTTP и фоновая обработка задач с Celery и Redis.

Работа объединяет компоненты из предыдущих лабораторных:

| Компонент | Источник |
|-----------|----------|
| FastAPI-приложение CollabPlatform | ЛР1 |
| Парсер веб-страниц | ЛР2 |
| Docker, Celery, Redis | ЛР3 |

## Цели

1. Упаковать FastAPI, PostgreSQL и парсер в Docker-контейнеры.
2. Реализовать HTTP-сервис парсера и вызов из основного API.
3. Организовать асинхронный парсинг через очередь Celery + Redis.

## Быстрый старт (Docker Compose)

```bash
cd lr3
docker compose up --build
```

После запуска доступны:

| Сервис | URL |
|--------|-----|
| CollabPlatform API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| Parser Service | http://localhost:8001 |
| Parser Swagger | http://localhost:8001/docs |
| PostgreSQL | localhost:5432 |
| Redis | localhost:6379 |

## Структура проекта

```
lr3/
├── app/                    # FastAPI (ЛР1) + эндпоинты парсера
│   ├── api/parser.py
│   ├── celery_app.py
│   └── tasks/parse_tasks.py
├── parser_service/         # Отдельный HTTP-сервис парсера
├── docker-compose.yml
├── Dockerfile.api
├── Dockerfile.parser
├── docs/                   # Документация MkDocs
├── mkdocs.yml
└── requirements.txt
```

## Содержание документации

- [Установка и запуск](setup.md)
- [Подзадача 1 — Docker](task1-docker.md)
- [Подзадача 2 — Вызов парсера из FastAPI](task2-parser.md)
- [Подзадача 3 — Celery и Redis](task3-celery.md)
- [Описание API](api.md)
- [Архитектура системы](architecture.md)

## Автор

Тимаков Егор, группа K3341, ИТМО, 2026
