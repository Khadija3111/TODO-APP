from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)

import uuid
from typing import TYPE_CHECKING

# For compatibility with Pydantic v2 and SQLModel
def generate_uuid() -> str:
    return str(uuid.uuid4())

def get_current_datetime() -> datetime:
    return datetime.now()

class User(UserBase, table=True):
    id: str = Field(default_factory=generate_uuid, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=get_current_datetime)
    updated_at: datetime = Field(default_factory=get_current_datetime)

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")

class UserCreate(UserBase):
    email: str
    password: str

class UserRead(UserBase):
    id: str
    created_at: datetime

class UserUpdate(SQLModel):
    email: Optional[str] = None