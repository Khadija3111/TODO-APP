"""
Test script for multi-turn conversations and database persistence
This script tests that conversations persist correctly in the database across multiple turns
"""

import asyncio
import json
from backend.api.chat import chat, ChatRequest
from backend.services.conversation_service import ConversationService
from backend.services.message_service import MessageService
from backend.utils.database import get_session
from sqlmodel import Session
from uuid import uuid4


async def test_multi_turn_conversations():
    """Test multi-turn conversations and database persistence"""

    print("Testing multi-turn conversations and database persistence...")

    # Create a test user ID
    user_id = str(uuid4())

    # Get a database session
    with next(get_session()) as session:
        conversation_service = ConversationService(session)
        message_service = MessageService(session)

        # Test 1: Create initial conversation and add first message
        print("\n1. Creating initial conversation and adding first message:")
        initial_request = ChatRequest(
            conversation_id=None,  # New conversation
            message="Add a task to buy groceries"
        )

        # We'll simulate calling the chat endpoint logic directly
        from backend.agents.chat_agent import run_chat_agent
        agent_response = await run_chat_agent(
            user_id=user_id,
            user_message=initial_request.message,
            conversation_history=[]
        )

        print(f"Agent response: {agent_response['response'][:100]}...")

        # Get or create conversation
        conversation = await conversation_service.create_conversation(user_id)
        conversation_id = str(conversation.id)
        print(f"Created conversation with ID: {conversation_id}")

        # Add user message to conversation
        user_message = await message_service.add_user_message(
            conversation_id=conversation_id,
            user_id=user_id,
            content=initial_request.message
        )
        print(f"Added user message: {user_message.content[:50]}...")

        # Add assistant response to conversation
        assistant_message = await message_service.add_assistant_message(
            conversation_id=conversation_id,
            user_id=user_id,
            content=agent_response.get("response", ""),
            tool_calls=agent_response.get("tool_calls", []),
            tool_results=agent_response.get("tool_results", [])
        )
        print(f"Added assistant message: {assistant_message.content[:50]}...")

        # Test 2: Get conversation history for next turn
        print("\n2. Getting conversation history for second turn:")
        conversation_history = await conversation_service.get_conversation_history_for_agent(conversation_id)
        print(f"Retrieved {len(conversation_history)} messages from history")
        for i, msg in enumerate(conversation_history):
            print(f"  Message {i+1}: {msg['role']} - {msg['content'][:50]}...")

        # Test 3: Second turn with conversation history
        print("\n3. Processing second turn with conversation history:")
        second_request = ChatRequest(
            conversation_id=conversation_id,
            message="What tasks do I have?"
        )

        second_agent_response = await run_chat_agent(
            user_id=user_id,
            user_message=second_request.message,
            conversation_history=conversation_history
        )

        print(f"Second agent response: {second_agent_response['response'][:100]}...")

        # Add second user message
        second_user_message = await message_service.add_user_message(
            conversation_id=conversation_id,
            user_id=user_id,
            content=second_request.message
        )
        print(f"Added second user message: {second_user_message.content[:50]}...")

        # Add second assistant response
        second_assistant_message = await message_service.add_assistant_message(
            conversation_id=conversation_id,
            user_id=user_id,
            content=second_agent_response.get("response", ""),
            tool_calls=second_agent_response.get("tool_calls", []),
            tool_results=second_agent_response.get("tool_results", [])
        )
        print(f"Added second assistant message: {second_assistant_message.content[:50]}...")

        # Test 4: Verify conversation persistence
        print("\n4. Verifying conversation persistence:")
        stored_messages = await message_service.get_conversation_messages(conversation_id)
        print(f"Total stored messages in DB: {len(stored_messages)}")

        for i, msg in enumerate(stored_messages):
            print(f"  Stored message {i+1}: {msg.role.value} - {msg.content[:50]}...")
            if msg.tool_calls:
                print(f"    Tool calls: {len(msg.tool_calls)}")
            if msg.tool_results:
                print(f"    Tool results: {len(msg.tool_results)}")

        # Test 5: Retrieve conversation by ID
        print("\n5. Retrieving conversation by ID:")
        retrieved_conversation = await conversation_service.get_conversation_by_id(conversation_id)
        if retrieved_conversation:
            print(f"Successfully retrieved conversation: {retrieved_conversation.id}")
            print(f"User ID: {retrieved_conversation.user_id}")
            print(f"Created at: {retrieved_conversation.created_at}")
        else:
            print("ERROR: Could not retrieve conversation by ID")

        # Test 6: Get user's conversations
        print("\n6. Getting all conversations for user:")
        user_conversations = await conversation_service.get_user_conversations(user_id)
        print(f"User has {len(user_conversations)} conversation(s)")

        print("\nMulti-turn conversation testing completed!")


if __name__ == "__main__":
    asyncio.run(test_multi_turn_conversations())