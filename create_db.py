# create_db.py

# Импортируем движок и базовый класс моделей
from app.database import engine, Base

# Импортируем модели, чтобы они зарегистрировались в metadata
from app import models

# Выводим сообщение перед созданием таблиц
print("Создаём таблицы в базе данных...")

# Создаём все таблицы, описанные в models.py
Base.metadata.create_all(bind=engine)

# Подтверждаем, что всё готово
print("✅ Таблицы успешно созданы.")
