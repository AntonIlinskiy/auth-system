from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.config import settings

from app.config import settings

SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.jwtsecret_key, algorithms=[settings.jwtalgorithm])
        exp = payload.get("exp")
        if exp is None or datetime.utcnow().timestamp() > exp:
            return None
        return payload
    except JWTError:
        return None