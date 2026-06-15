# Авторизация

Реализован полный функционал пользователя (задание на 15 баллов) **без сторонних библиотек для аутентификации** (fastapi-users, python-jose и т.п.). Используются только:

- **passlib + bcrypt** — хэширование паролей
- **PyJWT** — создание и проверка JWT-токенов

## Регистрация

`POST /auth/register` создаёт пользователя с хэшированным паролем.

```python
# app/core/security.py
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
```

## Вход и JWT

При успешном входе генерируется access token:

```python
def create_access_token(data: dict, expires_delta=None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
```

В payload токена передаётся `sub` — ID пользователя.

## Аутентификация по JWT (вручную)

Зависимость `get_current_user` в `app/core/deps.py` реализована вручную:

1. Извлекает заголовок `Authorization: Bearer <token>` через `HTTPBearer`
2. Декодирует токен функцией `decode_access_token`
3. Получает `user_id` из поля `sub`
4. Загружает пользователя из БД
5. Проверяет `is_active`

```python
def get_current_user(credentials, session) -> User:
    payload = decode_access_token(credentials.credentials)
    user_id = payload.get("sub")
    user = session.get(User, int(user_id))
    if not user.is_active:
        raise HTTPException(status_code=403, ...)
    return user
```

## Защищённые эндпоинты

Все CRUD-операции (кроме публичных GET) используют:

```python
current_user: Annotated[User, Depends(get_current_active_user)]
```

## Дополнительные методы

| Эндпоинт | Описание |
|----------|----------|
| `GET /auth/me` | Информация о текущем пользователе |
| `GET /users/` | Список всех пользователей |
| `GET /users/{id}` | Пользователь по ID |
| `POST /users/change-password` | Смена пароля |

### Смена пароля

```json
POST /users/change-password
Authorization: Bearer <token>

{
  "current_password": "old_secret",
  "new_password": "new_secret"
}
```

Проверяется текущий пароль через `verify_password`, новый сохраняется в хэшированном виде.

## Переменные окружения

| Переменная | Описание |
|------------|----------|
| `SECRET_KEY` | Секрет для подписи JWT |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Время жизни токена (по умолчанию 60) |

!!! warning
    В продакшене обязательно смените `SECRET_KEY` на криптографически стойкое значение.
