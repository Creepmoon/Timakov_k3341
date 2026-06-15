# Модель данных

В проекте реализовано **8 таблиц** с отношениями one-to-many и many-to-many.

## ER-диаграмма

```mermaid
erDiagram
    USER ||--o| PROFILE : has
    USER ||--o{ PROJECT : creates
    USER ||--o{ TEAM_MEMBER : participates
    USER ||--o{ TASK : assigned
    PROFILE ||--o{ PROFILE_SKILL_LINK : has
    SKILL ||--o{ PROFILE_SKILL_LINK : linked
    PROJECT ||--o{ TEAM : contains
    PROJECT ||--o{ TASK : has
    TEAM ||--o{ TEAM_MEMBER : includes

    USER {
        int id PK
        string email UK
        string username UK
        string hashed_password
        bool is_active
        datetime created_at
    }

    PROFILE {
        int id PK
        int user_id FK UK
        string bio
        int experience_years
        string interests
        string project_preferences
    }

    SKILL {
        int id PK
        string name UK
        string description
        enum category
    }

    PROFILE_SKILL_LINK {
        int profile_id PK_FK
        int skill_id PK_FK
        enum proficiency_level
    }

    PROJECT {
        int id PK
        int creator_id FK
        string title
        string description
        enum status
        datetime deadline
    }

    TEAM {
        int id PK
        int project_id FK
        string name
        string description
    }

    TEAM_MEMBER {
        int team_id PK_FK
        int user_id PK_FK
        enum role
        datetime joined_at
    }

    TASK {
        int id PK
        int project_id FK
        int assignee_id FK
        string title
        enum status
        int progress
        datetime deadline
    }
```

## Таблицы

### User
Учётная запись пользователя. Связь one-to-one с `Profile`.

### Profile
Расширенная информация о пользователе: биография, опыт, интересы, предпочтения по проектам.

### Skill
Справочник навыков (программирование, дизайн, менеджмент и т.д.).

### ProfileSkillLink (M2M)
Ассоциативная таблица между профилем и навыком.

| Поле | Описание |
|------|----------|
| `profile_id` | FK на профиль |
| `skill_id` | FK на навык |
| **`proficiency_level`** | Уровень владения: beginner / intermediate / advanced / expert |

### Project
Проект с целями, требованиями и ожидаемыми результатами. Создатель — `User` (one-to-many).

### Team
Команда, привязанная к проекту (one-to-many: Project → Team).

### TeamMember (M2M)
Ассоциативная таблица между командой и пользователем.

| Поле | Описание |
|------|----------|
| `team_id` | FK на команду |
| `user_id` | FK на пользователя |
| **`role`** | Роль: lead / developer / designer / manager / member |
| `joined_at` | Дата вступления |

### Task
Задача внутри проекта с дедлайном, статусом и прогрессом (0–100%).

## Типы связей

| Связь | Тип | Пример |
|-------|-----|--------|
| User → Profile | One-to-One | У каждого пользователя один профиль |
| User → Project | One-to-Many | Пользователь создаёт несколько проектов |
| Project → Team | One-to-Many | В проекте несколько команд |
| Project → Task | One-to-Many | В проекте много задач |
| Profile ↔ Skill | Many-to-Many | Через `ProfileSkillLink` |
| Team ↔ User | Many-to-Many | Через `TeamMember` |
