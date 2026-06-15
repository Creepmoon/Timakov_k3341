# Установка и настройка

## Требования

- Python 3.10+
- Доступ в интернет (для задачи 2)
- PostgreSQL 14+ — опционально, для интеграции с ЛР1 (CollabPlatform, папка `../lr1`)

## 1. Виртуальное окружение

```bash
cd students/K3341/Timakov_Egor/lr2
python -m venv venv
```

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

## 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

Основные пакеты:

| Пакет | Назначение |
|-------|------------|
| `requests` | HTTP-запросы (threading, multiprocessing) |
| `aiohttp` | Асинхронные HTTP-запросы |
| `beautifulsoup4` | Парсинг HTML |
| `sqlmodel` | ORM и работа с БД |
| `python-dotenv` | Переменные окружения |
| `mkdocs`, `mkdocs-material` | Документация |

## 3. Переменные окружения

Скопируйте шаблон:

```bash
copy .env.example .env     # Windows
cp .env.example .env       # Linux / macOS
```

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `DB_URL` | Строка подключения к БД | `sqlite:///parsed_pages.db` |
| `QUICK_MODE` | Быстрый режим для задачи 1 (`1` / `0`) | `1` |
| `NUM_WORKERS` | Число потоков / процессов | `4` |

### База данных

**SQLite (по умолчанию)** — файл `task2/parsed_pages.db`, не требует установки сервера.

**PostgreSQL из ЛР1** — укажите в `.env`:

```env
DB_URL=postgresql://postgres:123@localhost/collab_platform_db
```

Таблица `parsed_page` создаётся автоматически при первом запуске парсера.

## 4. Запуск программ

### Задача 1

```bash
cd task1
python threading_sum.py
python multiprocessing_sum.py
python async_sum.py
```

### Задача 2

```bash
cd task2
python threading_parser.py
python multiprocessing_parser.py
python async_parser.py
```

## 5. Документация MkDocs

Сборка и локальный просмотр:

```bash
mkdocs serve
```

Статическая сборка в папку `site/`:

```bash
mkdocs build
```

!!! note "Быстрый режим задачи 1"
    По заданию диапазон — от 1 до `10_000_000_000_000`. Полный перебор в цикле
    на таком объёме нереалистичен, поэтому по умолчанию `QUICK_MODE=1` и
    `N = 50_000_000`. Для полного диапазона: `QUICK_MODE=0`.
