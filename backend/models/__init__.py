# Import models to ensure they are registered with SQLModel metadata
# This helps avoid circular import issues

# Import models but handle circular dependencies by importing selectively
# First import base classes without table definitions
from .user import UserBase, UserCreate, UserRead, UserUpdate
from .task import TaskBase, TaskCreate, TaskRead, TaskUpdate, PriorityEnum
from .conversation import Conversation, Message, MessageRole

# Then import the main models with a mechanism to avoid duplicate table registration
# We'll import them separately to make sure relationships work
from .user import User  # This will be imported once globally
from .task import Task  # This will be imported once globally

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
    "PriorityEnum",
    "Conversation",
    "Message",
    "MessageRole"
]