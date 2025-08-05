from fastapi import Depends, HTTPException, status
from jose import JWTError
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.auth.jwt_handler import verify_access_token
from app.auth.schemas import TokenData


# Получение текущего пользователя по access token
def get_current_user(
    token: str = Depends(verify_access_token),
    db: Session = Depends(get_db),
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token_data = TokenData(**token)
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    if user is None or not user.is_active:
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
