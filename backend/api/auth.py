from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from datetime import timedelta
from sqlmodel import Session, select
from typing import Optional
from ..database import get_session
from ..models.user import User, UserCreate, UserRead, UserLogin
from ..utils.password import get_password_hash, verify_password
from ..utils.auth import create_access_token
from ..config import settings

router = APIRouter()

@router.post("/register", response_model=UserRead)
async def register(user: UserCreate, session: Session = Depends(get_session)):
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Hash password and create user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        name=user.name,
        password_hash=hashed_password
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.post("/login")
async def login(user_credentials: UserLogin, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == user_credentials.email)).first()
    if not user or not verify_password(user_credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create JWT token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name
        }
    }

@router.post("/logout")
async def logout(credentials: HTTPAuthorizationCredentials = Depends(HTTPAuthorizationCredentials)):
    # In a real implementation, you might add the token to a blacklist
    # For now, we just return a success message
    return {"message": "Successfully logged out"}