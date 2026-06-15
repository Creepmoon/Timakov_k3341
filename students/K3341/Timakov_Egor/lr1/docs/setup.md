# Установка и запуск

## Требования

- Python 3.10+
- PostgreSQL 14+

## 1. Клонирование и виртуальное окружение

```bash
cd students/K3341/Timakov_Egor/lr1
python -m venv venv
```

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/macOS:**
```bash
source venv/bin/activate
```

## 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

## 3. Настройка PostgreSQL

Создайте базу данных:

```sql
CREATE DATABASE collab_platform_db;
```

Скопируйте файл окружения и укажите параметры подключения:

```bash
copy .env.example .env
```

Пример `.env`:

```
DB_URL=postgresql://postgres:123@localhost/collab_platform_db
SECRET_KEY=your-super-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## 4. Миграции Alembic

```bash
alembic upgrade head
```

Для создания новой миграции после изменения моделей:

```bash
alembic revision --autogenerate -m "описание изменений"
alembic upgrade head
```

!!! note
    URL базы данных в `alembic.ini` переопределяется из `.env` в файле `migrations/env.py` через `python-dotenv`.

## 5. Запуск сервера

```bash
uvicorn app.main:app --reload
```

| URL | Описание |
|-----|----------|
| http://127.0.0.1:8000 | Корневой эндпоинт |
| http://127.0.0.1:8000/docs | Swagger UI |
| http://127.0.0.1:8000/redoc | ReDoc |

## 6. Документация MkDocs

```bash
mkdocs serve
```

Документация будет доступна на http://127.0.0.1:8001

## Практика 1.1 (отдельная папка)

```bash
cd practice_1_1
uvicorn main:app --reload --port 8001
```
