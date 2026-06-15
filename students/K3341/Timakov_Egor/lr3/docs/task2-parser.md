# Подзадача 2 — Вызов парсера из FastAPI

## Цель

Добавить в основное FastAPI-приложение (CollabPlatform) эндпоинт, который принимает URL от клиента, отправляет запрос сервису парсера в отдельном контейнере и возвращает результат.

## Реализация

Маршрут: `POST /parser/parse?url=<URL>`

Файл: `app/api/parser.py`

```python
@router.post("/parse")
def parse_sync(url: str) -> dict:
  response = requests.post(
    f"{settings.PARSER_URL}/parse",
    params={"url": url},
    timeout=60,
  )
  response.raise_for_status()
  return response.json()
```

URL сервиса парсера задаётся переменной окружения `PARSER_URL`:

- локально: `http://localhost:8001`
- в Docker Compose: `http://parser:8001` (имя сервиса в сети Compose)

## Схема взаимодействия

```
Клиент  →  POST /parser/parse  →  API (порт 8000)
                                      ↓ HTTP
                                 Parser (порт 8001)
                                      ↓
                                 PostgreSQL (parsed_page)
```

## Пример запроса

```bash
curl -X POST "http://localhost:8000/parser/parse?url=https://example.com"
```

Ответ:

```json
{
  "message": "Parsing completed",
  "url": "https://example.com",
  "title": "Example Domain"
}
```

## Swagger UI

Интерактивная документация: [http://localhost:8000/docs](http://localhost:8000/docs) — раздел **parser**.

## Обработка ошибок

При недоступности целевой страницы или сервиса парсера API возвращает HTTP 500 с описанием ошибки в поле `detail`.
