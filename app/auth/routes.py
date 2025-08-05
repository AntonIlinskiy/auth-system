from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.logic import create_user
from app.auth.schemas import UserCreate, UserOut
from app.models import User
from passlib.context import CryptContext

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


