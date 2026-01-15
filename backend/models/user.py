from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

# For compatibility with Pydantic v2 and SQLModel
def generate_uuid():
    return str(uuid.uuid4())

def get_current_datetime():
    return datetime.now()

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)

class User(UserBase, table=True):
    id: str = Field(default=None, primary_key=True)
    # email field is inherited from UserBase
    hashed_password: str
    created_at: datetime = Field(default=None)
    updated_at: datetime = Field(default=None)

    # Relationship to tasks - using string reference to avoid circular import
    tasks: List["Task"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

    def __init__(self, **data):
        super().__init__(**data)
        if self.id is None:
            self.id = generate_uuid()
        if self.created_at is None:
            self.created_at = get_current_datetime()
        if self.updated_at is None:
            self.updated_at = get_current_datetime()

class UserCreate(UserBase):
    email: str
    password: str

class UserRead(SQLModel):
    id: str
    email: str
    created_at: datetime

class UserUpdate(SQLModel):
    email: Optional[str] = None