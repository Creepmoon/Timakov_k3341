# Подзадача 3 — Celery и Redis

## Цель

Организовать фоновую обработку задач парсинга через асинхронную очередь Celery с брокером Redis.

## Компоненты

| Компонент | Роль |
|-----------|------|
| **Redis** | Брокер сообщений и хранилище результатов Celery |
| **Celery worker** | Выполняет задачи парсинга в фоне |
| **FastAPI** | Принимает запрос, ставит задачу в очередь, отдаёт `task_id` |

## Конфигурация Celery

Файл `app/celery_app.py`:

```python
celery_app = Celery(
  "collab_platform",
  broker=settings.CELERY_BROKER_URL,
  backend=settings.CELERY_RESULT_BACKEND,
  include=["app.tasks.parse_tasks"],
)
```

Переменные окружения:

- `CELERY_BROKER_URL=redis://redis:6379/0`
- `CELERY_RESULT_BACKEND=redis://redis:6379/1`

## Задача парсинга

Файл `app/tasks/parse_tasks.py`:

```python
@celery_app.task(name="parse_url")
def parse_url_task(url: str) -> dict:
  response = requests.post(f"{settings.PARSER_URL}/parse", params={"url": url})
  response.raise_for_status()
  return response.json()
```

Worker вызывает тот же HTTP-сервис парсера, что и синхронный эндпоинт — единая точка логики парсинга.

## Эндпоинты API

### Постановка задачи в очередь

`POST /parser/parse/async?url=<URL>`

```bash
curl -X POST "http://localhost:8000/parser/parse/async?url=https://example.com"
```

Ответ:

```json
{
  "message": "Parsing started",
  "task_id": "a1b2c3d4-...",
  "url": "https://example.com"
}
```

### Проверка статуса

`GET /parser/parse/status/{task_id}`

```bash
curl "http://localhost:8000/parser/parse/status/a1b2c3d4-..."
```

Возможные статусы: `PENDING`, `STARTED`, `SUCCESS`, `FAILURE`.

Пример успешного результата:

```json
{
  "task_id": "a1b2c3d4-...",
  "status": "SUCCESS",
  "result": {
    "message": "Parsing completed",
    "url": "https://example.com",
    "title": "Example Domain"
  }
}
```

## Docker Compose

В `docker-compose.yml` добавлены:

- сервис `redis` с healthcheck;
- сервис `celery_worker` на базе `Dockerfile.api` с командой  
  `celery -A app.celery_app worker --loglevel=info`.

## Зачем очередь задач

- Длительный парсинг не блокирует HTTP-ответ клиенту.
- Можно масштабировать число worker-ов.
- Redis + Celery — стандартный стек для фоновых задач в Python-проектах.
