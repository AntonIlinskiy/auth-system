from sqlalchemy.orm import Session
from app.models import User
from app.auth.hashing import hash_password
from app.auth.schemas import UserCreate
from fastapi import HTTPException, status
from app.auth.hashing import verify_password
from sqlalchemy import select
from app import models
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User

def create_user(db: Session, user: UserCreate):
    hashed_pw = hash_password(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_pw,
        first_name=user.first_name,
        last_name=user.last_name,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

async def authenticate_user(email: str, password: str, db: AsyncSession):
    stmt = select(User).where(User.email == User.email)
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()

    if not existing_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not User.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    if not verify_password(password, User.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return User