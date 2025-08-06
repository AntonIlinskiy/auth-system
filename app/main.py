# Импортируем FastAPI - основной класс приложения
from fastapi import FastAPI, Depends
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from app.auth.routes import router as auth_router
from app.database import engine
from app.models import Base
import sys
import os
from app.auth_control.routes import router as admin_router



app = FastAPI()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(self, tokenUrl: str):
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl})
        super().__init__(flows=flows)

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/login")


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

class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(self, tokenUrl: str):
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl})
        super().__init__(flows=flows)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="My Auth App",
        version="1.0.0",
        description="Custom Auth System",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", []).append({"BearerAuth": []})
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app.include_router(auth_router)

app.include_router(admin_router)
