# Описание API

## CollabPlatform API (порт 8000)

Базовый URL: `http://localhost:8000`

Полная документация CollabPlatform из ЛР1 доступна в Swagger: `/docs`.

### Эндпоинты парсера (ЛР3)

| Метод | Путь | Описание |
|-------|------|----------|
| `POST` | `/parser/parse` | Синхронный парсинг URL через сервис парсера |
| `POST` | `/parser/parse/async` | Асинхронный парсинг через Celery |
| `GET` | `/parser/parse/status/{task_id}` | Статус и результат фоновой задачи |

Все эндпоинты принимают параметр `url` (query string).

### Примеры

**Синхронный парсинг:**

```http
POST /parser/parse?url=https://www.python.org
```

**Асинхронный парсинг:**

```http
POST /parser/parse/async?url=https://www.python.org
```

**Статус задачи:**

```http
GET /parser/parse/status/{task_id}
```

---

## Parser Service (порт 8001)

Базовый URL: `http://localhost:8001`

| Метод | Путь | Описание |
|-------|------|----------|
| `GET` | `/` | Health check |
| `POST` | `/parse` | Парсинг URL и сохранение в БД |

Swagger: [http://localhost:8001/docs](http://localhost:8001/docs)

### Тело ответа `/parse`

```json
{
  "message": "Parsing completed",
  "url": "https://example.com",
  "title": "Example Domain"
}
```

### Коды ошибок

| Код | Причина |
|-----|---------|
| 500 | Ошибка HTTP-запроса к целевой странице или внутренняя ошибка парсера |

## Модель данных `parsed_page`

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | int | Первичный ключ |
| `url` | str | URL страницы (уникальный) |
| `title` | str | Заголовок `<title>` |
| `parsed_at` | datetime | Время парсинга |
