from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.auth.jwt_handler import verify_access_token
from app.auth.schemas import TokenData
from app.models import User
from app.config import settings
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Получение текущего пользователя по access token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user


# Проверка разрешения на действие с конкретным ресурсом
def check_permission(resource: str, action: str):
    def permission_checker(current_user: models.User = Depends(get_current_user)):
        for role in current_user.roles:
            for permission in role.permissions:
                if permission.resource == resource and permission.action == action:
                    return  # доступ разрешён
        raise HTTPException(status_code=403, detail="Forbidden")
    return permission_checker
