# API

Все защищённые эндпоинты требуют заголовок `Authorization: Bearer <token>`.

## Auth — `/auth`

| Метод | Путь | Описание | Auth |
|-------|------|----------|------|
| POST | `/auth/register` | Регистрация | — |
| POST | `/auth/login` | Вход, получение JWT | — |
| GET | `/auth/me` | Текущий пользователь | ✓ |

### Регистрация

```json
POST /auth/register
{
  "email": "user@example.com",
  "username": "dev_user",
  "password": "secret123"
}
```

### Вход

```json
POST /auth/login
{
  "email": "user@example.com",
  "password": "secret123"
}
```

Ответ:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

## Users — `/users`

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/users/` | Список пользователей |
| GET | `/users/{id}` | Пользователь по ID |
| PATCH | `/users/{id}` | Обновление (только свой) |
| POST | `/users/change-password` | Смена пароля |

## Profiles — `/profiles`

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/profiles/` | Список с фильтрами |
| GET | `/profiles/{id}` | Профиль с навыками (вложенные) |
| POST | `/profiles/` | Создание |
| PATCH | `/profiles/{id}` | Обновление |
| DELETE | `/profiles/{id}` | Удаление |
| POST | `/profiles/skills` | Добавить навык к профилю |
| PATCH | `/profiles/skills/{profile_id}/{skill_id}` | Обновить уровень |
| DELETE | `/profiles/skills/{profile_id}/{skill_id}` | Удалить навык |

### Фильтры поиска профилей

| Параметр | Тип | Описание |
|----------|-----|----------|
| `skill_id` | int | Навык |
| `min_experience` | int | Минимальный опыт (лет) |
| `interests` | str | Подстрока в интересах |

### Пример ответа с вложенными объектами

```json
GET /profiles/1
{
  "id": 1,
  "user_id": 1,
  "bio": "Full-stack разработчик",
  "experience_years": 3,
  "interests": "веб, стартапы",
  "project_preferences": "open-source",
  "user": {
    "id": 1,
    "username": "alex",
    "email": "alex@example.com"
  },
  "skills": [
    {
      "skill_id": 1,
      "proficiency_level": "advanced",
      "skill": {
        "id": 1,
        "name": "Python",
        "description": "Backend",
        "category": "programming"
      }
    }
  ]
}
```

## Skills — `/skills`

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/skills/` | Список (фильтры: category, name) |
| GET | `/skills/{id}` | Навык |
| POST | `/skills/` | Создание |
| PATCH | `/skills/{id}` | Обновление |
| DELETE | `/skills/{id}` | Удаление |

## Projects — `/projects`

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/projects/` | Список (фильтры: status, creator_id, title) |
| GET | `/projects/{id}` | Проект с командами и задачами |
| POST | `/projects/` | Создание |
| PATCH | `/projects/{id}` | Обновление |
| DELETE | `/projects/{id}` | Удаление |

### Пример вложенного ответа

```json
GET /projects/1
{
  "id": 1,
  "title": "CollabApp",
  "creator": { "id": 1, "username": "alex", "email": "..." },
  "teams": [
    {
      "id": 1,
      "name": "Backend Team",
      "members": [
        {
          "team_id": 1,
          "user_id": 2,
          "role": "developer",
          "user": { "id": 2, "username": "maria", "email": "..." }
        }
      ]
    }
  ],
  "tasks": [
    {
      "id": 1,
      "title": "Настроить CI",
      "status": "in_progress",
      "progress": 50,
      "assignee": { "id": 2, "username": "maria", "email": "..." }
    }
  ]
}
```

## Teams — `/teams`

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/teams/` | Список команд с участниками |
| GET | `/teams/{id}` | Команда |
| POST | `/teams/` | Создание |
| PATCH | `/teams/{id}` | Обновление |
| DELETE | `/teams/{id}` | Удаление |
| POST | `/teams/members` | Добавить участника |
| PATCH | `/teams/members/{team_id}/{user_id}` | Изменить роль |
| DELETE | `/teams/members/{team_id}/{user_id}` | Удалить участника |

## Tasks — `/tasks`

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/tasks/` | Список (фильтры: project_id, assignee_id, status) |
| GET | `/tasks/{id}` | Задача |
| POST | `/tasks/` | Создание |
| PATCH | `/tasks/{id}` | Обновление |
| DELETE | `/tasks/{id}` | Удаление |
