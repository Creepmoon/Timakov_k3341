# Практики 1.1–1.3

Каждая практика реализована в отдельной папке / этапе проекта.

## Практика 1.1 — Базовое FastAPI-приложение

**Папка:** `practice_1_1/`

Реализовано:

- GET `/` — приветствие
- Временная БД (`temp_bd`) с 2 профилями
- CRUD для профилей (`/profiles_list`, `/profile/{id}`, POST, PUT, DELETE)
- Pydantic-модели: `Profile`, `Skill`, `ProfilePreferences`
- Вложенный объект (`preferences`) и список объектов (`skills`)
- Отдельное API для навыков (`/skills_list`, `/skill/{id}`, POST)
- Аннотация типов и `response_model`

Запуск:
```bash
cd practice_1_1
uvicorn main:app --reload --port 8001
```

## Практика 1.2 — SQLModel и PostgreSQL

**Папка:** `app/`

Реализовано:

- Подключение к PostgreSQL (`app/core/database.py`)
- SQLModel-модели с отношениями one-to-many и many-to-many
- Ассоциативные сущности с дополнительными полями:
  - `ProfileSkillLink.proficiency_level`
  - `TeamMember.role`
- CRUD через сессии SQLModel и `Depends(get_session)`
- GET-запросы с вложенными объектами через `response_model` (схемы в `app/schemas/responses.py`)
- PATCH для частичного обновления

## Практика 1.3 — Миграции, ENV, структура

Реализовано:

- **Alembic:** `migrations/`, `alembic.ini`, начальная миграция `001_initial.py`
- **`.env`:** переменные `DB_URL`, `SECRET_KEY` через `python-dotenv`
- **`.gitignore`:** исключены `venv/`, `*.env`, `__pycache__/`, `site/`
- **Структура проекта:** разделение на `api/`, `core/`, `models/`, `schemas/`
- URL БД для Alembic передаётся из `.env` в `migrations/env.py`

### Команды миграций

```bash
# Применить все миграции
alembic upgrade head

# Создать новую миграцию
alembic revision --autogenerate -m "описание"

# Откатить
alembic downgrade -1
```

## Лабораторная работа (9 + 15 баллов)

Помимо практик, реализовано полное серверное приложение:

| Критерий | Статус |
|----------|--------|
| 5+ таблиц | ✓ 8 таблиц |
| One-to-many | ✓ User→Project, Project→Team, Project→Task |
| Many-to-many | ✓ Profile↔Skill, Team↔User |
| Ассоциативная сущность с полем связи | ✓ proficiency_level, role |
| CRUD API | ✓ Все сущности |
| Вложенные GET | ✓ Profile, Project, Team |
| Alembic | ✓ |
| Аннотация типов | ✓ |
| Файловая структура | ✓ |
| JWT авторизация | ✓ |
| Регистрация / смена пароля | ✓ |
| Ручная аутентификация JWT | ✓ |
