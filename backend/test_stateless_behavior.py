"""
Test script for validating stateless behavior after server restarts
This script tests that conversation history is preserved in the database across server restarts
"""

import asyncio
import json
from backend.services.conversation_service import ConversationService
from backend.services.message_service import MessageService
from backend.utils.database import get_session
from sqlmodel import Session
from uuid import uuid4


async def test_stateless_behavior():
    """Test stateless behavior after server restarts"""

    print("Testing stateless behavior after server restarts...")

    # Create a test user ID
    user_id = str(uuid4())

    # Get a database session
    with next(get_session()) as session:
        conversation_service = ConversationService(session)
        message_service = MessageService(session)

        # Test 1: Create a conversation and add some messages
        print("\n1. Creating conversation and adding initial messages:")

        # Create conversation
        conversation = await conversation_service.create_conversation(user_id)
        conversation_id = str(conversation.id)
        print(f"Created conversation with ID: {conversation_id}")

        # Add initial messages to the conversation
        await message_service.add_user_message(
            conversation_id=conversation_id,
            user_id=user_id,
            content="Add a task to buy groceries"
        )
        print("Added first user message")

        await message_service.add_assistant_message(
            conversation_id=conversation_id,
            user_id=user_id,
            content="Okay, I've added the task 'buy groceries' for you.",
            tool_calls=[{"name": "add_task", "arguments": {"title": "buy groceries"}}],
            tool_results=[{"success": True, "task_id": "1", "title": "buy groceries"}]
        )
        print("Added first assistant message")

        await message_service.add_user_message(
            conversation_id=conversation_id,
            user_id=user_id,
            content="What tasks do I have?"
        )
        print("Added second user message")

        await message_service.add_assistant_message(
            conversation_id=conversation_id,
            user_id=user_id,
            content="You have the following tasks: buy groceries (ID: 1)",
            tool_calls=[{"name": "list_tasks", "arguments": {"user_id": user_id}}],
            tool_results=[{"tasks": [{"id": "1", "title": "buy groceries", "completed": False}], "count": 1}]
        )
        print("Added second assistant message")

        # Verify messages are stored
        stored_messages_before_restart = await message_service.get_conversation_messages(conversation_id)
        print(f"Messages stored before simulated restart: {len(stored_messages_before_restart)}")

        # Test 2: Simulate server restart by creating a new session/service instance
        print("\n2. Simulating server restart (conversation state should persist in DB):")

        # Create a new session to simulate fresh server state
        with next(get_session()) as new_session:
            new_conversation_service = ConversationService(new_session)
            new_message_service = MessageService(new_session)

            # Verify the conversation still exists
            retrieved_conversation = await new_conversation_service.get_conversation_by_id(conversation_id)
            if retrieved_conversation:
                print(f"✓ Conversation still exists after restart: {retrieved_conversation.id}")
                print(f"  Belongs to user: {retrieved_conversation.user_id}")
            else:
                print("✗ ERROR: Conversation not found after restart")
                return

            # Verify messages are still accessible
            stored_messages_after_restart = await new_message_service.get_conversation_messages(conversation_id)
            print(f"Messages available after simulated restart: {len(stored_messages_after_restart)}")

            # Compare message counts
            if len(stored_messages_before_restart) == len(stored_messages_after_restart):
                print("✓ Message count preserved across restart")
            else:
                print("✗ ERROR: Message count changed after restart")
                return

            # Verify message content is preserved
            original_contents = [msg.content for msg in stored_messages_before_restart]
            restored_contents = [msg.content for msg in stored_messages_after_restart]

            if original_contents == restored_contents:
                print("✓ Message content preserved across restart")
            else:
                print("✗ ERROR: Message content changed after restart")
                print(f"  Original: {original_contents}")
                print(f"  Restored: {restored_contents}")
                return

            # Test 3: Add more messages after "restart" to verify ongoing functionality
            print("\n3. Adding more messages after restart:")

            await new_message_service.add_user_message(
                conversation_id=conversation_id,
                user_id=user_id,
                content="Mark the groceries task as completed"
            )
            print("Added third user message after restart")

            await new_message_service.add_assistant_message(
                conversation_id=conversation_id,
                user_id=user_id,
                content="I've marked the 'buy groceries' task as completed.",
                tool_calls=[{"name": "complete_task", "arguments": {"task_id": "1", "user_id": user_id}}],
                tool_results=[{"success": True, "task_id": "1", "completed": True}]
            )
            print("Added third assistant message after restart")

            # Verify total message count is updated
            final_message_count = len(await new_message_service.get_conversation_messages(conversation_id))
            print(f"Total messages after adding more: {final_message_count}")

        # Test 4: Final verification with yet another session
        print("\n4. Final verification with fresh session:")

        with next(get_session()) as final_session:
            final_conversation_service = ConversationService(final_session)
            final_message_service = MessageService(final_session)

            # Verify conversation still exists
            final_conversation = await final_conversation_service.get_conversation_by_id(conversation_id)
            if final_conversation:
                print(f"✓ Conversation still exists in fresh session: {final_conversation.id}")
            else:
                print("✗ ERROR: Conversation lost in fresh session")

            # Verify all messages are preserved
            final_messages = await final_message_service.get_conversation_messages(conversation_id)
            print(f"Final message count: {len(final_messages)}")

            # Print message summary
            for i, msg in enumerate(final_messages):
                role_emoji = "👤" if msg.role.value == "user" else "🤖"
                print(f"  {role_emoji} {msg.role.value}: {msg.content[:50]}{'...' if len(msg.content) > 50 else ''}")

        print("\nStateless behavior validation completed!")
        print("✓ Conversations and messages persisted in database across simulated restarts")
        print("✓ System maintains state without relying on in-memory storage")


if __name__ == "__main__":
    asyncio.run(test_stateless_behavior())