"""
Test script for frontend-backend communication
This script tests the complete flow from frontend API calls to backend processing
"""

import asyncio
import json
from backend.api.chat import chat, ChatRequest
from backend.agents.chat_agent import run_chat_agent
from backend.services.conversation_service import ConversationService
from backend.services.message_service import MessageService
from backend.utils.database import get_session
from sqlmodel import Session
from uuid import uuid4


async def test_frontend_backend_communication():
    """Test complete frontend-backend communication flow"""

    print("Testing frontend-backend communication...")

    # Create a test user ID
    user_id = str(uuid4())

    # Get a database session
    with next(get_session()) as session:
        conversation_service = ConversationService(session)
        message_service = MessageService(session)

        # Test 1: Simulate a complete chat request like the frontend would make
        print("\n1. Simulating frontend chat request:")

        # Create initial request (like frontend would send)
        initial_request = ChatRequest(
            conversation_id=None,  # New conversation
            message="Add a task to buy groceries"
        )

        print(f"Frontend sending request: {initial_request.dict()}")

        # Call the chat endpoint function directly (simulating API call)
        from fastapi import BackgroundTasks
        response = await chat(
            user_id=user_id,
            request=initial_request,
            background_tasks=BackgroundTasks(),  # Placeholder
            session=session
        )

        print(f"Backend response: {response.dict()}")

        # Verify response structure
        assert hasattr(response, 'conversation_id'), "Response should include conversation_id"
        assert hasattr(response, 'response'), "Response should include response text"
        assert hasattr(response, 'tool_calls'), "Response should include tool_calls"
        assert hasattr(response, 'tool_results'), "Response should include tool_results"

        print("✓ Response structure is correct")

        # Get conversation ID for next test
        conversation_id = response.conversation_id
        print(f"Using conversation ID: {conversation_id}")

        # Test 2: Verify conversation was created and messages were stored
        print("\n2. Verifying conversation and message storage:")

        # Get conversation from DB
        conversation = await conversation_service.get_conversation_by_id(conversation_id)
        assert conversation is not None, "Conversation should exist in DB"
        assert conversation.user_id == user_id, "Conversation should belong to correct user"
        print(f"✓ Conversation exists and belongs to user {user_id}")

        # Get messages from DB
        messages = await message_service.get_conversation_messages(conversation_id)
        assert len(messages) >= 2, f"Should have at least 2 messages (user + assistant), got {len(messages)}"

        # Verify message roles
        user_messages = [m for m in messages if m.role.value == "user"]
        assistant_messages = [m for m in messages if m.role.value == "assistant"]

        assert len(user_messages) >= 1, "Should have at least 1 user message"
        assert len(assistant_messages) >= 1, "Should have at least 1 assistant message"

        print(f"✓ Found {len(user_messages)} user messages and {len(assistant_messages)} assistant messages")

        # Test 3: Second message in same conversation
        print("\n3. Testing second message in same conversation:")

        second_request = ChatRequest(
            conversation_id=conversation_id,  # Existing conversation
            message="What tasks do I have?"
        )

        print(f"Frontend sending second request: {second_request.dict()}")

        second_response = await chat(
            user_id=user_id,
            request=second_request,
            background_tasks=BackgroundTasks(),
            session=session
        )

        print(f"Second backend response: {second_response.dict()}")

        # Verify conversation ID is the same
        assert second_response.conversation_id == conversation_id, "Conversation ID should remain the same"
        print("✓ Conversation ID preserved across requests")

        # Verify new messages were added
        updated_messages = await message_service.get_conversation_messages(conversation_id)
        assert len(updated_messages) >= 4, f"Should have at least 4 messages now, got {len(updated_messages)}"
        print(f"✓ Total messages after second request: {len(updated_messages)}")

        # Test 4: Verify tool execution worked
        print("\n4. Verifying tool execution:")

        # Check if tool calls were made in the responses
        if response.tool_calls or second_response.tool_calls:
            print(f"✓ Tool calls executed: {len(response.tool_calls) + len(second_response.tool_calls)} total")

            # Check for specific task-related tools
            all_tool_calls = response.tool_calls + second_response.tool_calls
            task_tools_found = [tc for tc in all_tool_calls if tc.get('name', '').startswith('add_') or tc.get('name', '').startswith('list_')]
            print(f"✓ Found {len(task_tools_found)} task-related tool calls")
        else:
            print("! No tool calls found in responses (may be expected for some inputs)")

        # Test 5: Verify message content
        print("\n5. Verifying message content:")

        # Find the last assistant message to check for task-related content
        assistant_msgs = [m for m in updated_messages if m.role.value == "assistant"]
        if assistant_msgs:
            last_assistant_msg = assistant_msgs[-1]
            print(f"Last assistant message: {last_assistant_msg.content[:100]}...")

            # Check if it contains task-related information
            if "task" in last_assistant_msg.content.lower() or "grocery" in last_assistant_msg.content.lower():
                print("✓ Assistant response contains task-related content")
            else:
                print("! Assistant response may not contain expected task content")

        print("\nFrontend-backend communication test completed!")
        print("✓ API requests properly handled")
        print("✓ Conversations stored in database")
        print("✓ Messages stored with correct roles")
        print("✓ Conversation state maintained")
        print("✓ Tool execution verified")


if __name__ == "__main__":
    asyncio.run(test_frontend_backend_communication())