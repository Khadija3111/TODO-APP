"""
Service layer for message management
Handles business logic for storing and retrieving messages
"""

import json
from typing import List, Optional
from datetime import datetime
from sqlmodel import Session, select

from models.conversation import Message, MessageRole
from utils.database import (
    get_conversation_session,
    add_message_to_conversation as db_add_message_to_conversation,
    get_conversation_messages as db_get_conversation_messages,
    get_recent_conversation_messages as db_get_recent_conversation_messages
)


class MessageService:
    def __init__(self, session: Session):
        self.session = session

    async def add_message(
        self,
        conversation_id: str,
        user_id: str,
        role: MessageRole,
        content: str,
        tool_calls: Optional[List[dict]] = None,
        tool_results: Optional[List[dict]] = None
    ) -> Message:
        """
        Add a message to a conversation
        """
        # Serialize tool_calls and tool_results to JSON strings
        tool_calls_json = json.dumps(tool_calls) if tool_calls else None
        tool_results_json = json.dumps(tool_results) if tool_results else None

        return db_add_message_to_conversation(
            conversation_id,
            user_id,
            role,
            content,
            tool_calls=tool_calls_json,
            tool_results=tool_results_json
        )

    async def add_user_message(
        self,
        conversation_id: str,
        user_id: str,
        content: str
    ) -> Message:
        """
        Add a user message to a conversation
        """
        return await self.add_message(
            conversation_id,
            user_id,
            MessageRole.USER,
            content,
            tool_calls=None,
            tool_results=None
        )

    async def add_assistant_message(
        self,
        conversation_id: str,
        user_id: str,
        content: str,
        tool_calls: Optional[List[dict]] = None,
        tool_results: Optional[List[dict]] = None
    ) -> Message:
        """
        Add an assistant message to a conversation with optional tool calls and results
        """
        return await self.add_message(
            conversation_id,
            user_id,
            MessageRole.ASSISTANT,
            content,
            tool_calls=tool_calls,
            tool_results=tool_results
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

    async def format_messages_for_display(self, messages: List[Message]) -> List[dict]:
        """
        Format messages for display in the frontend
        """
        formatted_messages = []
        for msg in messages:
            formatted_message = {
                "id": msg.id,
                "role": msg.role.value,
                "content": msg.content,
                "created_at": msg.created_at.isoformat(),
                "user_id": msg.user_id
            }

            # Include tool_calls and tool_results if they exist (deserialize from JSON)
            if msg.tool_calls is not None:
                try:
                    formatted_message["tool_calls"] = json.loads(msg.tool_calls)
                except (json.JSONDecodeError, TypeError):
                    formatted_message["tool_calls"] = msg.tool_calls
            if msg.tool_results is not None:
                try:
                    formatted_message["tool_results"] = json.loads(msg.tool_results)
                except (json.JSONDecodeError, TypeError):
                    formatted_message["tool_results"] = msg.tool_results

            formatted_messages.append(formatted_message)
        return formatted_messages

    async def get_formatted_conversation_history(
        self,
        conversation_id: str
    ) -> List[dict]:
        """
        Get conversation history formatted for display
        """
        messages = await self.get_conversation_messages(conversation_id)
        return await self.format_messages_for_display(messages)