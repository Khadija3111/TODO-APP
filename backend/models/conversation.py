"""
SQLModel definitions for Conversation and Message entities
Used for chatbot conversation history and message storage
"""

from datetime import datetime
from typing import Optional, List, Any
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
import sqlmodel.sql.sqltypes
import uuid


class MessageRole(str, Enum):
    """
    Enum for message roles in conversation
    """
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Conversation(SQLModel, table=True):
    """
    Conversation model for tracking chat sessions
    """
    id: Optional[str] = Field(default=None, sa_column_kwargs={"primary_key": True})  # Using string to store UUID
    user_id: str = Field(index=True)  # Index for efficient querying by user
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to messages
    messages: list["Message"] = Relationship(back_populates="conversation")


def generate_message_uuid():
    return str(uuid.uuid4())

def get_current_message_datetime():
    return datetime.now()

class Message(SQLModel, table=True):
    """
    Message model for storing conversation history
    """
    id: Optional[str] = Field(default=None, sa_column_kwargs={"primary_key": True})  # Using string to store UUID
    user_id: str = Field(index=True)  # Index for efficient querying by user
    conversation_id: str = Field(foreign_key="conversation.id", index=True)  # Foreign key reference
    role: MessageRole = Field(sa_column_kwargs={"default": MessageRole.USER})
    content: str
    tool_calls: Optional[str] = Field(default=None)  # Store tool calls made as JSON string
    tool_results: Optional[str] = Field(default=None)  # Store results from tool calls as JSON string
    created_at: datetime = Field(default=None)

    # Relationship to conversation
    conversation: Optional[Conversation] = Relationship(back_populates="messages")

    def __init__(self, **data):
        super().__init__(**data)
        if self.id is None:
            self.id = generate_message_uuid()
        if self.created_at is None:
            self.created_at = get_current_message_datetime()