# Импорртируем FastAPI - основной класс приложения
from fastapi import FastAPI, Depends
from app.config import settings
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import routes as auth_routes
from app.auth.routes import router as auth_router
from app.mock_views import router as mock_router
from app.database import engine
from app.models import Base
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# Импортируем экземпляр приложения FastAPI
app = FastAPI(
    title="Auth System with Custom RBAC",
    version="1.0.0",
)


# Простой маршрут, чтобы проверять, что сервер запущен и БД работает
@app.get("/")
def root():
    return "Auth system is running"

app.include_router(auth_router)
app.include_router(mock_router)

print(">>> DATABASE_URL:", settings.DATABASE_URL)