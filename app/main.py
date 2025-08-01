# Импорртируем FastAPI - основной класс приложения
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import routes as auth_routes

# Импорртируем экземпляр приложения FastAPI
app = FastAPI()

# Простой маршрут, чтобы проверять, что сервер запущен и БД работает
@app.get("/")
def root():
    return "Auth system is running"

app.include_router(auth_routes.router)