# Импорртируем FastAPI - основной класс приложения
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import get_db

# Импорртируем экземпляр приложения FastAPI
app = FastAPI()

# Простой маршрут, чтобы проверять, что сервер запущен и БД работает
@app.get("/")
def root(db: Session = Depends(get_db)):
    return {"message": "Database connected!"}