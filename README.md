🔐 Auth System (FastAPI + PostgreSQL)
Проект авторизации и аутентификации с собственной RBAC-моделью — кастомные роли, разрешения и управление доступом к ресурсам.

🚀 Стек
Python 3.12

FastAPI

SQLAlchemy (sync)

PostgreSQL

Alembic

Uvicorn

python-jose (JWT)

Pydantic

📌 Функциональность
👤 Пользователь
Регистрация (/register)

Авторизация (/login)

Обновление профиля (PUT /me)

Мягкое удаление аккаунта (DELETE /me)

Logout — через удаление токена на клиенте

Получение текущего пользователя (GET /me)

🔐 JWT
Выдача токена при логине

Проверка авторизации по Bearer-токену

Обработка 401 (Unauthorized) и 403 (Forbidden)

🎯 Ролевая модель (RBAC)
Пользователь может иметь одну или несколько ролей

Каждая роль содержит разрешения (resource + action)

Проверка доступа к эндпоинтам через зависимость has_permission(...)

Мок-ресурсы (/resources/...) защищены ролями

💾 Структура БД
📂 Таблицы
Таблица	Описание
users	Пользователи системы
roles	Роли (например: admin, manager, user)
permissions	Разрешения (users:read, roles:create)
user_roles	Связь User <-> Role
role_permissions	Связь Role <-> Permission

📜 Примеры прав и ролей
json
Копировать
Редактировать
[
  {
    "role": "admin",
    "permissions": [
      { "resource": "users", "action": "read" },
      { "resource": "users", "action": "update" },
      { "resource": "users", "action": "delete" },
      { "resource": "roles", "action": "create" },
      { "resource": "roles", "action": "read" },
      { "resource": "permissions", "action": "create" },
      { "resource": "permissions", "action": "read" }
    ]
  },
  {
    "role": "user",
    "permissions": [
      { "resource": "profile", "action": "read" },
      { "resource": "profile", "action": "update" }
    ]
  }
]
🔒 Защита эндпоинтов
Метод	Путь	Роль / Права
GET	/me	Любой авторизованный
GET	/auth_control/roles	roles:read
GET	/auth_control/permissions	permissions:read
POST	/auth_control/roles	roles:create
POST	/auth_control/permissions	permissions:create
POST	/auth_control/users/{id}/roles/{id}	users:update

🧪 Примеры curl
bash
Копировать
Редактировать
# 🔐 Login
curl -X POST http://127.0.0.1:8000/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=admin123"

# ✅ Получить профиль
curl http://127.0.0.1:8000/me \
  -H "Authorization: Bearer <TOKEN>"

# 🛡️ Получить роли (если есть права)
curl http://127.0.0.1:8000/auth_control/roles \
  -H "Authorization: Bearer <TOKEN>"
🧪 Тестовые данные
✅ Предустановленные пользователи:
Email	Пароль	Роль
admin@example.com	admin123	admin
user@example.com	user123	user

📌 scripts/seed_data.py создаёт роли и права автоматически

🔧 Быстрый старт
bash
Копировать
Редактировать
# Клонировать проект
git clone https://github.com/AntonIlinskiy/auth-system.git
cd auth-system

# Создать окружение
python -m venv .venv
source .venv/bin/activate  # или .venv\Scripts\activate для Windows

# Установить зависимости
pip install -r requirements.txt

# .env
cp .env.example .env  # и заполни

# Применить миграции
alembic upgrade head

# Засеять БД правами и ролями
python -m app.scripts.seed_data

# Запуск сервера
uvicorn app.main:app --reload
✅ Что реализовано
 Регистрация и логин

 JWT-авторизация

 Проверка доступа (401/403)

 Ролевая модель (RBAC)

 Назначение ролей пользователям

 Защита эндпоинтов

 MockView ресурсы

 Тестовые роли и права

 README.md с документацией

🧪 Юнит-тесты (опционально)
Папка tests/ может содержать тесты:

test_register.py

test_login.py

test_rbac.py

👤 Автор
@Anton Ilinskiy