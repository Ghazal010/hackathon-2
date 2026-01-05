from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from passlib.context import CryptContext
from enum import Enum

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    name: Optional[str] = Field(default=None)

class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password_hash)

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None

class UserLogin(SQLModel):
    email: str
    password: str