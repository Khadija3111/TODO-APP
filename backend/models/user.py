from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

# For compatibility with Pydantic v2 and SQLModel
def generate_uuid() -> str:
    return str(uuid.uuid4())

def get_current_datetime() -> datetime:
    return datetime.now()

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)

class User(UserBase, table=True):
    id: str = Field(default_factory=generate_uuid, primary_key=True)
    # email field is inherited from UserBase
    hashed_password: str
    created_at: datetime = Field(default_factory=get_current_datetime)
    updated_at: datetime = Field(default_factory=get_current_datetime)

    # Relationship to tasks - using string reference to avoid circular import
    tasks: List["Task"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

class UserCreate(UserBase):
    email: str
    password: str

class UserRead(SQLModel):
    id: str
    email: str
    created_at: datetime

class UserUpdate(SQLModel):
    email: Optional[str] = None