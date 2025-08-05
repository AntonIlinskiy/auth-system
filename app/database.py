from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from app.config import settings
from fastapi import Depends
import os

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем строку подключения к ДБ из переменноых окружения
DATABASE_URL = settings.DATABASE_URL

# Создаем движок SQL Alchemy - управляет подключением к БД
engine = create_engine(DATABASE_URL)
# Фабрика сессий - для создания подключения к БД в каждом запросе
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для всех моделей SQLAlchemy
Base = declarative_base()

# Функция для подключения к БД в маршрутах через Depends
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()