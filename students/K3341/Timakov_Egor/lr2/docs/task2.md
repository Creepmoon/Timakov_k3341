# Задача 2 — Парсинг веб-страниц

Параллельная загрузка веб-страниц, извлечение заголовка `<title>` и сохранение в базу данных.

## Постановка

- Три программы: `threading`, `multiprocessing`, `asyncio` + `aiohttp`
- Функция `parse_and_save(url)` — загрузка, парсинг, сохранение
- Список URL разбивается для параллельной обработки
- Данные сохраняются в БД (SQLite или PostgreSQL из ЛР1)

## Файлы

| Файл | Назначение |
|------|------------|
| `task2/common.py` | `parse_and_save()`, `fetch_html()`, `extract_title()` |
| `task2/models.py` | SQLModel-модель `ParsedPage` |
| `task2/database.py` | Подключение к БД, `init_db()` |
| `task2/urls.py` | Список URL и `NUM_WORKERS` |
| `task2/threading_parser.py` | Вариант на потоках |
| `task2/multiprocessing_parser.py` | Вариант на процессах |
| `task2/async_parser.py` | Вариант на asyncio + aiohttp |

## Модель данных

Таблица `parsed_page`:

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | int, PK | Идентификатор |
| `url` | str, unique | Адрес страницы |
| `title` | str | Заголовок из `<title>` |
| `parsed_at` | datetime | Время парсинга |

```python
class ParsedPage(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  url: str = Field(index=True, unique=True)
  title: str
  parsed_at: datetime = Field(default_factory=datetime.utcnow)
```

## Функция `parse_and_save(url)`

```mermaid
sequenceDiagram
    participant P as parse_and_save
    participant W as Веб-сервер
    participant DB as База данных

    P->>W: HTTP GET url
    W-->>P: HTML
    P->>P: extract_title(html)
    P->>DB: INSERT / UPDATE parsed_page
    P-->>P: print результат
```

Шаги:

1. Загрузка HTML (`requests` или `aiohttp`)
2. Извлечение заголовка через BeautifulSoup
3. Сохранение в БД (создание или обновление записи по URL)
4. Вывод `[OK] url -> title` в консоль

При сетевой ошибке выводится `[FAIL]` без остановки остальных задач.

## Список URL

В `task2/urls.py` задано 12 адресов:

- python.org, docs.python.org
- fastapi.tiangolo.com, flask, django
- postgresql.org, example.com, github.com, pypi.org
- quotes.toscrape.com, books.toscrape.com (учебные сайты для парсинга)
- httpbin.org/html

## Реализации

### Threading

- `ThreadPoolExecutor` с `NUM_WORKERS` потоками
- HTTP через библиотеку `requests`
- Пока один поток ждёт ответ сервера, другие продолжают работу

### Multiprocessing

- `ProcessPoolExecutor` — каждый URL обрабатывается в отдельном процессе
- Тот же `parse_and_save()` из `common.py`
- Выше накладные расходы на создание процессов

### Asyncio + aiohttp

```python
async def parse_and_save(session, url):
  async with session.get(url) as response:
    html = await response.text()
  title = extract_title(html)
  await asyncio.to_thread(save_title, url, title)
```

- Все HTTP-запросы выполняются **конкурентно** в одном потоке
- Запись в БД вынесена в `asyncio.to_thread()`, чтобы не блокировать event loop

## Запуск

```bash
cd task2
python threading_parser.py
python multiprocessing_parser.py
python async_parser.py
```

## Подключение к PostgreSQL (ЛР1)

В файле `.env`:

```env
DB_URL=postgresql://postgres:123@localhost/collab_platform_db
```

Таблица `parsed_page` будет создана в той же базе, что используется в CollabPlatform.

Результаты замеров — в разделе [Замеры и сравнение](benchmarks.md).
