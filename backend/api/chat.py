"""
Chat API endpoint for the AI Chatbot
Handles user requests and communicates with the AI agent
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from sqlmodel import Session
from datetime import datetime

from models.conversation import MessageRole
from services.conversation_service import ConversationService
from services.message_service import MessageService
from utils.database import get_session
from agents.chat_agent import run_chat_agent

router = APIRouter()


class ChatRequest(BaseModel):
    """
    Request model for chat endpoint
    """
    conversation_id: Optional[str] = None
    message: str


class ChatResponse(BaseModel):
    """
    Response model for chat endpoint
    """
    conversation_id: str
    response: str
    tool_calls: List[Dict[str, Any]] = []
    tool_results: List[Dict[str, Any]] = []


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    request: ChatRequest,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session)
) -> ChatResponse:
    """
    Main chat endpoint that processes user messages and returns AI responses
    """
    conversation_service = ConversationService(session)
    message_service = MessageService(session)

    # Get or create conversation
    if request.conversation_id is None:
        # Create new conversation
        conversation = await conversation_service.create_conversation(user_id)
        conversation_id = str(conversation.id)
    else:
        # Validate that conversation exists and belongs to user
        conversation = await conversation_service.get_conversation_by_id(request.conversation_id)
        if not conversation or str(conversation.user_id) != user_id:
            raise HTTPException(status_code=404, detail="Conversation not found")
        conversation_id = str(conversation.id)

    # Add user message to conversation
    user_message = await message_service.add_user_message(
        conversation_id=conversation_id,
        user_id=user_id,
        content=request.message
    )

    # Get conversation history for the agent
    conversation_history = await conversation_service.get_conversation_history_for_agent(conversation_id)

    # Run the chat agent to get response
    try:
        agent_response = await run_chat_agent(
            user_id=user_id,
            user_message=request.message,
            conversation_history=conversation_history
        )

        response_text = agent_response.get("response", "")
        tool_calls = agent_response.get("tool_calls", [])
        tool_results = agent_response.get("tool_results", [])
    except Exception as e:
        # If agent fails, return a generic error response
        response_text = f"Sorry, I encountered an error processing your request: {str(e)}"
        tool_calls = []
        tool_results = []

    # Add assistant response to conversation
    assistant_message = await message_service.add_assistant_message(
        conversation_id=conversation_id,
        user_id=user_id,
        content=response_text,
        tool_calls=tool_calls,
        tool_results=tool_results
    )

    return ChatResponse(
        conversation_id=conversation_id,
        response=response_text,
        tool_calls=tool_calls,
        tool_results=tool_results
    )


@router.get("/{user_id}/conversations")
async def get_user_conversations(
    user_id: str,
    session: Session = Depends(get_session)
):
    """
    Get all conversations for a user
    """
    conversation_service = ConversationService(session)
    conversations = await conversation_service.get_user_conversations(user_id)

    return [
        {
            "id": conv.id,
            "user_id": conv.user_id,
            "created_at": conv.created_at.isoformat(),
            "updated_at": conv.updated_at.isoformat()
        }
        for conv in conversations
    ]


@router.get("/{user_id}/conversations/{conversation_id}")
async def get_conversation_messages(
    user_id: str,
    conversation_id: str,
    session: Session = Depends(get_session)
):
    """
    Get messages for a specific conversation
    """
    conversation_service = ConversationService(session)
    message_service = MessageService(session)

    # Verify conversation belongs to user
    conversation = await conversation_service.get_conversation_by_id(conversation_id)
    if not conversation or str(conversation.user_id) != user_id:
        raise HTTPException(status_code=404, detail="Conversation not found")

    messages = await message_service.get_formatted_conversation_history(conversation_id)
    return {
        "conversation_id": conversation_id,
        "messages": messages
    }