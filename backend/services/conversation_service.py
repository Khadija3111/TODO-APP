"""
Service layer for conversation management
Handles business logic for conversations and messages
"""

from typing import List, Optional
from datetime import datetime
from sqlmodel import Session, select

from models.conversation import Conversation, Message, MessageRole
from utils.database import (
    get_conversation_session,
    create_conversation as db_create_conversation,
    get_conversation_by_id as db_get_conversation_by_id,
    get_user_conversations as db_get_user_conversations,
    add_message_to_conversation as db_add_message_to_conversation,
    get_conversation_messages as db_get_conversation_messages,
    get_recent_conversation_messages as db_get_recent_conversation_messages,
    update_conversation_timestamp as db_update_conversation_timestamp
)


class ConversationService:
    def __init__(self, session: Session):
        self.session = session

    async def create_conversation(self, user_id: str) -> Conversation:
        """
        Create a new conversation for a user
        """
        return db_create_conversation(user_id)

    async def get_conversation_by_id(self, conversation_id: str) -> Optional[Conversation]:
        """
        Get a conversation by its ID
        """
        return db_get_conversation_by_id(conversation_id)

    async def get_user_conversations(self, user_id: str) -> List[Conversation]:
        """
        Get all conversations for a specific user
        """
        return db_get_user_conversations(user_id)

    async def add_user_message(
        self,
        conversation_id: str,
        user_id: str,
        content: str
    ) -> Message:
        """
        Add a user message to a conversation
        """
        return db_add_message_to_conversation(
            conversation_id,
            user_id,
            MessageRole.USER,
            content
        )

    async def add_assistant_message(
        self,
        conversation_id: str,
        user_id: str,
        content: str
    ) -> Message:
        """
        Add an assistant message to a conversation
        """
        return db_add_message_to_conversation(
            conversation_id,
            user_id,
            MessageRole.ASSISTANT,
            content
        )

    async def get_conversation_messages(self, conversation_id: str) -> List[Message]:
        """
        Get all messages for a specific conversation
        """
        return db_get_conversation_messages(conversation_id)

    async def get_recent_conversation_messages(
        self,
        conversation_id: str,
        limit: int = 50
    ) -> List[Message]:
        """
        Get recent messages for a specific conversation with a limit
        """
        return db_get_recent_conversation_messages(conversation_id, limit)

    async def get_conversation_history_for_agent(
        self,
        conversation_id: str
    ) -> List[dict]:
        """
        Get conversation history formatted for the AI agent
        """
        messages = await self.get_conversation_messages(conversation_id)

        formatted_history = []
        for msg in messages:
            formatted_history.append({
                "role": msg.role.value,
                "content": msg.content
            })

        return formatted_history

    async def update_conversation_timestamp(self, conversation_id: str):
        """
        Update the updated_at timestamp for a conversation
        """
        db_update_conversation_timestamp(conversation_id)