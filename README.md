# 🔐 Auth System (FastAPI + PostgreSQL)

Проект авторизации и аутентификации с кастомной системой прав доступа, ролевой моделью, JWT-токенами и управлением пользователями.

---

## 🚀 Стек

- Python 3.12
- FastAPI
- SQLAlchemy (sync)
- PostgreSQL
- Alembic
- Uvicorn
- python-jose (JWT)
- Pydantic

# 🚀 Функциональность

### 👤 Пользователь
- Регистрация (`/register`)
- Авторизация (`/login`)
- Обновление профиля (`PUT /me`)
- Мягкое удаление аккаунта (`DELETE /me`)
- Logout — через удаление токена на клиенте

### 🔐 JWT
- Выдача токена при логине
- Проверка авторизации по `Bearer`-токену
- Обработка 401 и 403 ошибок

### 🎯 Авторизация (RBAC)
- Пользователь имеет роли и разрешения
- Можно назначать права на доступ к ресурсам
- Ресурсы — моковые (`/resources/...`) с проверкой прав
- 403 Forbidden при недостатке прав

---

## 💾 Модели в базе

### `users`
| Поле         | Тип        | Описание                      |
|--------------|------------|-------------------------------|
| id           | UUID       | Уникальный идентификатор     |
| email        | str        | Email (уникальный)           |
| password     | str        | Хэш пароля                   |
| first_name   | str        | Имя                          |
| last_name    | str        | Фамилия                      |
| is_active    | bool       | Активен или soft-deleted     |

### `roles`, `permissions`, `user_roles`, `role_permissions`
(Опционально: если реализовано RBAC)
---

## ⚙️ Быстрый старт

```bash
# Клонируем репозиторий
git clone https://github.com/AntonIlinskiy/auth-system.git
cd auth-system

# Создаём и активируем виртуальное окружение
python -m venv .venv
.venv\Scripts\activate  # Windows

# Устанавливаем зависимости
pip install -r requirements.txt

# Создаём .env
cp .env.example .env

# Применяем миграции
alembic upgrade head

# Запускаем сервер
python -m app.main
```

---

## 🔒 API endpoints

| Метод | Путь              | Описание                      | Доступ       |
|-------|-------------------|-------------------------------|--------------|
| POST  | `/register`       | Регистрация пользователя      | Публичный    |
| POST  | `/login`          | Вход, JWT                     | Публичный    |
| GET   | `/me`             | Получение текущего пользователя | Авторизован |
| PATCH | `/users/{id}`     | Обновление пользователя       | Владелец     |
| DELETE| `/users/{id}`     | Удаление пользователя         | Владелец     |
| GET   | `/admin/users`    | Получение всех пользователей  | Админ        |

---

## ✅ Выполнено

- [x] Регистрация пользователя
- [x] Хэширование пароля
- [x] Подключение PostgreSQL
- [x] Alembic миграции
- [x] Работающая модель User
- [x] Запуск и тестирование


## 🧑‍💻 Автор

[@AntonIlinskiy](https://github.com/AntonIlinskiy)
