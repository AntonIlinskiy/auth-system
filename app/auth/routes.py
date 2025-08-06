from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.schemas import UserCreate, UserOut, UserLogin, UserUpdate
from passlib.context import CryptContext
from app.auth.utils import verify_password, create_access_token, get_current_user, hash_password
from datetime import datetime, timedelta
from jose import jwt
from app.config import settings
from app.auth.utils import get_current_user
from app.models import User
from app.auth.utils import authenticate_user


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


router = APIRouter()

@router.post("/register", response_model=UserOut)


def register(user: UserCreate, db: Session = Depends(get_db)):
    print(">>> REGISTER DATA:", user.dict())  # для отладки
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pw = hash_password(user.password)
    db_user = User(
        email=user.email,
        password=hashed_pw,
        first_name=user.first_name,
        last_name=user.last_name
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: int = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=expires_delta if expires_delta is not None else settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(user_data.email, user_data.password, db)

    if not user or not user.is_active:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


def read_users_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name
    }

@router.put("me", response_model=UserOut)

def update_user(
        user_update: UserUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    # обновление email, имени, фамилии
        if user_update.email:
            current_user.email = user_update.email
        if user_update.first_name:
            current_user.first_name = user_update.first_name
        if user_update.last_name:
            current_user.last_name = user_update.last_name

        if user_update.password:
            current_user.password = CryptContext(schemes=["bcrypt"], deprecated="auto").hash(user_update.password)

        db.commit()
        db.refresh(current_user)
        return current_user


@router.delete("/me")
def delete_user(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
        current_user.is_active = False
        db.commit()
        return {"message": "User deactivated (soft deleted)"}


@router.get("/me", response_model=UserOut)
def read_current_user(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return current_user