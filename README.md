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

---

## 📌 План на завтра

- [ ] 🔑 Вход по email/password — endpoint `/login`
- [ ] 🔐 JWT токен и проверка доступа к `/me`
- [ ] ✅ Обновление профиля пользователя
- [ ] ❌ Удаление пользователя (`DELETE /users/{user_id}`)
- [ ] 🛡️ Ограничение доступа по ролям (admin / user)
- [ ] 🧪 Юнит-тесты для регистрации, логина, удаления
- [ ] 📦 Docker + .env.production (опционально)

---

## 🧑‍💻 Автор

[@AntonIlinskiy](https://github.com/AntonIlinskiy)
