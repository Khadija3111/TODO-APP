from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from enum import Enum
import json

class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: Optional[PriorityEnum] = PriorityEnum.medium
    category: Optional[str] = None

import uuid

# For compatibility with Pydantic v2 and SQLModel
def generate_task_uuid() -> str:
    return str(uuid.uuid4())

def get_current_task_datetime() -> datetime:
    return datetime.now()

class Task(TaskBase, table=True):
    id: str = Field(default_factory=generate_task_uuid, primary_key=True)
    user_id: Optional[str] = Field(default=None, foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=get_current_task_datetime)
    updated_at: datetime = Field(default_factory=get_current_task_datetime)

    # Additional field for tags as JSON string
    tags: Optional[str] = Field(default=None)  # Storing tags as JSON string

    # Relationship to user
    user: Optional["User"] = Relationship(back_populates="tasks")

    @property
    def tags_list(self) -> list[str]:
        """Get the task tags as a list."""
        if self.tags:
            try:
                return json.loads(self.tags)
            except:
                return []
        return []

    def set_tags(self, tags: list[str]) -> None:
        """Set the task tags from a list."""
        self.tags = json.dumps(tags) if tags else None

    def add_tag(self, tag: str) -> None:
        """Add a tag to the task."""
        if not isinstance(tag, str):
            raise ValueError("Tag must be a string")
        tag = tag.strip()
        if not tag:
            raise ValueError("Tag cannot be empty or contain only whitespace")

        current_tags = self.tags_list
        if tag not in current_tags:
            current_tags.append(tag)
            self.set_tags(current_tags)

    def remove_tag(self, tag: str) -> bool:
        """Remove a tag from the task. Returns True if tag was found and removed."""
        current_tags = self.tags_list
        if tag in current_tags:
            current_tags.remove(tag)
            self.set_tags(current_tags)
            return True
        return False

class TaskCreate(TaskBase):
    title: str

class TaskRead(TaskBase):
    id: str
    user_id: Optional[str]
    created_at: datetime
    updated_at: datetime

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[PriorityEnum] = None
    category: Optional[str] = None