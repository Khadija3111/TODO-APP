from sqlmodel import create_engine, Session, SQLModel, select
import os
from typing import Optional
from contextlib import contextmanager
from datetime import datetime
from models.conversation import Conversation, Message, MessageRole

# Get database URL from environment variable (Railway sets this automatically with PostgreSQL addon)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")  # Fallback to SQLite for local dev

# Handle Railway's PostgreSQL URL format (convert postgres:// to postgresql://)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Configure engine with proper SSL settings for production
if "postgresql://" in DATABASE_URL:
    # Production PostgreSQL settings
    engine = create_engine(
        DATABASE_URL,
        echo=False,  # Set to True for debugging
        pool_pre_ping=True,
        pool_recycle=300,
        connect_args={
            "sslmode": "require",  # Require SSL for PostgreSQL
        }
    )
else:
    # Local SQLite settings
    engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


# Global flag to track if tables have been created
_tables_initialized = False

# Function to initialize the database tables
def create_db_and_tables():
    global _tables_initialized
    from sqlmodel import SQLModel

    # Only initialize tables once to avoid duplicate registration
    if not _tables_initialized:
        # Import models to ensure they're registered with SQLModel metadata
        # Import the table models directly to register them
        from models.user import User
        from models.task import Task
        from models.conversation import Conversation, Message

        # For SQLite development, we may need to recreate tables to update schema
        # Only do this for SQLite (development), not for production databases
        if "sqlite://" in DATABASE_URL:
            print("SQLite detected - dropping and recreating all tables for schema update")
            # Drop all tables and recreate them to ensure latest schema
            SQLModel.metadata.drop_all(engine)
        elif "postgresql://" in DATABASE_URL:
            print("PostgreSQL (Neon) detected - creating tables without dropping (preserving data)")
        else:
            print("Production database detected - creating tables without dropping")

        SQLModel.metadata.create_all(engine)
        print("Database tables created successfully")
        _tables_initialized = True


@contextmanager
def get_conversation_session():
    """
    Context manager for getting a database session specifically for conversation operations
    """
    with Session(engine) as session:
        yield session


import uuid

def create_conversation(user_id: str) -> Conversation:
    """
    Create a new conversation for a user
    """
    with get_conversation_session() as session:
        conversation_id = str(uuid.uuid4())
        conversation = Conversation(id=conversation_id, user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation


def get_conversation_by_id(conversation_id: str) -> Optional[Conversation]:
    """
    Get a conversation by its ID
    """
    with get_conversation_session() as session:
        statement = select(Conversation).where(Conversation.id == conversation_id)
        return session.exec(statement).first()


def get_user_conversations(user_id: str) -> list[Conversation]:
    """
    Get all conversations for a specific user
    """
    with get_conversation_session() as session:
        statement = select(Conversation).where(Conversation.user_id == user_id)
        return session.exec(statement).all()


def add_message_to_conversation(
    conversation_id: str,
    user_id: str,
    role: MessageRole,
    content: str,
    tool_calls: Optional[str] = None,
    tool_results: Optional[str] = None
) -> Message:
    """
    Add a message to a conversation
    """
    with get_conversation_session() as session:
        message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            content=content,
            tool_calls=tool_calls,
            tool_results=tool_results
        )
        session.add(message)
        session.commit()
        session.refresh(message)
        return message


def get_conversation_messages(conversation_id: str) -> list[Message]:
    """
    Get all messages for a specific conversation
    """
    with get_conversation_session() as session:
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc())
        return session.exec(statement).all()


def get_recent_conversation_messages(
    conversation_id: str,
    limit: int = 50
) -> list[Message]:
    """
    Get recent messages for a specific conversation with a limit
    """
    with get_conversation_session() as session:
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.desc()).limit(limit)
        messages = session.exec(statement).all()
        # Return in chronological order (oldest first)
        return list(reversed(messages))


def update_conversation_timestamp(conversation_id: str):
    """
    Update the updated_at timestamp for a conversation
    """
    with get_conversation_session() as session:
        conversation = session.get(Conversation, conversation_id)
        if conversation:
            conversation.updated_at = datetime.utcnow()
            session.add(conversation)
            session.commit()


def delete_conversation(conversation_id: str) -> bool:
    """
    Delete a conversation and all its messages
    """
    with get_conversation_session() as session:
        # First delete all messages in the conversation
        message_statement = select(Message).where(Message.conversation_id == conversation_id)
        messages = session.exec(message_statement).all()
        for message in messages:
            session.delete(message)

        # Then delete the conversation itself
        conversation = session.get(Conversation, conversation_id)
        if conversation:
            session.delete(conversation)
            session.commit()
            return True
        return False