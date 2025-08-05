from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List


#  Схема для регистрации нового пользователя
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str | None = None

    class Config:
        from_attributes = True


class UserCreateOut(BaseModel):
    id: int
    email: EmailStr
    last_name: str
    first_name: str
    is_active: bool






#  Схема для логина пользователя
class UserLogin(BaseModel):
    email: EmailStr
    password: str


#  Схема для возврата данных пользователя (например, /me)
class UserOut(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str | None = None
    is_active: bool

    class Config:
        from_attributes = True # Нужно для работы с SQLAlchemy-моделями


#  Схема токена (JWT)
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


#  Декодированный токен (при валидации токена)
class TokenData(BaseModel):
    user_id: Optional[int] = None


#  Схемы для прав и ролей — на будущее

class PermissionSchema(BaseModel):
    resource: str
    action: str

    class Config:
        from_attributes = True


class RoleSchema(BaseModel):
    id: int
    name: str
    permissions: List[PermissionSchema] = []

    class Config:
        from_attributes = True

class RegisterRequest(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str = Field(min_length=6)
    password_confirm: str = Field(min_length=6)

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool

    class Config:
        from_attributes = True


