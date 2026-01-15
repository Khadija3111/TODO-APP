# Import models to ensure they are registered with SQLModel metadata
# This helps avoid circular import issues

from .user import User, UserBase, UserCreate, UserRead, UserUpdate
from .task import Task, TaskBase, TaskCreate, TaskRead, TaskUpdate, PriorityEnum

__all__ = [
    "User",
    "UserBase",
    "UserCreate",
    "UserRead",
    "UserUpdate",
    "Task",
    "TaskBase",
    "TaskCreate",
    "TaskRead",
    "TaskUpdate",
    "PriorityEnum"
]