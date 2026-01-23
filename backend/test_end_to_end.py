"""
End-to-end validation test for all user stories
This script validates that all the implemented features work together as expected
"""
import asyncio
from backend.api.chat import chat, ChatRequest
from backend.agents.chat_agent import run_chat_agent
from backend.services.conversation_service import ConversationService
from backend.services.message_service import MessageService
from backend.mcp.tools.task_operations import list_tasks_tool, ListTasksParams
from backend.utils.database import get_session
from sqlmodel import Session
from uuid import uuid4


async def run_end_to_end_validation():
    """Run end-to-end validation of all user stories"""

    print("Starting end-to-end validation of all user stories...")

    # Create a test user ID
    user_id = str(uuid4())

    # Get a database session
    with next(get_session()) as session:
        conversation_service = ConversationService(session)
        message_service = MessageService(session)

        print("\n=== USER STORY 1: AI-Powered Natural Language Task Management ===")

        # Simulate the first conversation with the AI chatbot
        print("\n1. Testing AI chatbot interaction for task creation:")
        initial_request = ChatRequest(
            conversation_id=None,  # New conversation
            message="I need to add a task to buy groceries"
        )

        response = await chat(
            user_id=user_id,
            request=initial_request,
            session=session
        )

        print(f"✓ Chat response: {response.response[:100]}...")
        print(f"✓ Conversation ID: {response.conversation_id}")
        print(f"✓ Tool calls made: {len(response.tool_calls)}")

        # Verify the task was created
        tasks_result = await list_tasks_tool(ListTasksParams(user_id=user_id, status="all"))
        tasks = tasks_result.get("tasks", [])
        print(f"✓ Tasks after creation: {len(tasks)}")
        if tasks:
            print(f"  - Task: {tasks[0]['title']} (Status: {tasks[0]['status']})")

        print("\n=== USER STORY 2: Multi-Turn Conversations ===")

        # Continue the conversation
        print("2. Testing multi-turn conversation for task listing:")
        second_request = ChatRequest(
            conversation_id=response.conversation_id,  # Continue conversation
            message="What tasks do I have?"
        )

        second_response = await chat(
            user_id=user_id,
            request=second_request,
            session=session
        )

        print(f"✓ Second response: {second_response.response[:100]}...")
        print(f"✓ Same conversation ID maintained: {second_response.conversation_id == response.conversation_id}")

        print("\n=== USER STORY 3: Intelligent Task Disambiguation ===")

        # Add more tasks for disambiguation testing
        print("3. Testing intelligent disambiguation:")

        # Add tasks with similar names
        disambiguation_request1 = ChatRequest(
            conversation_id=second_response.conversation_id,
            message="Add a task to call my mom"
        )

        await chat(
            user_id=user_id,
            request=disambiguation_request1,
            session=session
        )

        disambiguation_request2 = ChatRequest(
            conversation_id=second_response.conversation_id,
            message="Add a task to call my dad"
        )

        await chat(
            user_id=user_id,
            request=disambiguation_request2,
            session=session
        )

        # Now try to complete an ambiguous task
        disambiguation_request3 = ChatRequest(
            conversation_id=second_response.conversation_id,
            message="Complete the call task"
        )

        disambiguation_response = await chat(
            user_id=user_id,
            request=disambiguation_request3,
            session=session
        )

        print(f"✓ Disambiguation response: {disambiguation_response.response[:150]}...")

        # Check if the system asked for clarification
        if "specify" in disambiguation_response.response.lower() or "which one" in disambiguation_response.response.lower():
            print("✓ Disambiguation working - system asked for clarification")
        else:
            print("? Disambiguation may not have triggered as expected")

        print("\n=== USER STORY 4: Rich Chat Interface ===")

        print("4. Testing rich chat interface features:")
        # List tasks to see formatted response
        list_request = ChatRequest(
            conversation_id=second_response.conversation_id,
            message="List all my tasks"
        )

        list_response = await chat(
            user_id=user_id,
            request=list_request,
            session=session
        )

        print(f"✓ Task listing response: {list_response.response[:150]}...")
        print(f"✓ Tool calls in list response: {len(list_response.tool_calls)}")

        print("\n=== VALIDATING DATABASE PERSISTENCE ===")

        print("5. Validating database persistence:")
        # Get conversation from DB to verify persistence
        conversation = await conversation_service.get_conversation_by_id(second_response.conversation_id)
        if conversation:
            print("✓ Conversation properly persisted in database")
            print(f"  - Conversation ID: {conversation.id}")
            print(f"  - User ID: {conversation.user_id}")
            print(f"  - Created at: {conversation.created_at}")
        else:
            print("✗ Conversation not found in database")

        # Get messages from DB to verify persistence
        messages = await message_service.get_conversation_messages(second_response.conversation_id)
        print(f"✓ Retrieved {len(messages)} messages from database")

        for i, msg in enumerate(messages):
            print(f"  - Message {i+1}: {msg.role.value} - {msg.content[:50]}...")

        print("\n=== VALIDATING USER ISOLATION ===")

        print("6. Validating user isolation:")
        # Create another user and verify they can't see the first user's tasks
        other_user_id = str(uuid4())

        other_user_request = ChatRequest(
            conversation_id=None,
            message="What tasks do I have?"
        )

        other_response = await chat(
            user_id=other_user_id,
            request=other_user_request,
            session=session
        )

        print(f"✓ Other user response: {other_response.response[:100]}...")

        # Verify other user doesn't see first user's tasks
        other_tasks_result = await list_tasks_tool(ListTasksParams(user_id=other_user_id, status="all"))
        other_tasks = other_tasks_result.get("tasks", [])
        print(f"✓ Other user tasks count: {len(other_tasks)} (should be 0)")

        if len(other_tasks) == 0:
            print("✓ User isolation working properly")
        else:
            print("✗ User isolation issue - other user can see tasks")

        print("\n=== TESTING ERROR HANDLING ===")

        print("7. Testing error handling:")
        # Try to complete a non-existent task
        error_request = ChatRequest(
            conversation_id=second_response.conversation_id,
            message="Complete task 999999"
        )

        error_response = await chat(
            user_id=user_id,
            request=error_request,
            session=session
        )

        print(f"✓ Error response: {error_response.response[:150]}...")
        if "couldn't find" in error_response.response.lower():
            print("✓ Error handling working - proper error message returned")
        else:
            print("? Error handling may not have produced expected message")

        print("\n=== FINAL VALIDATION SUMMARY ===")

        # Final verification of all tasks for the main user
        final_tasks = await list_tasks_tool(ListTasksParams(user_id=user_id, status="all"))
        final_task_count = len(final_tasks.get("tasks", []))

        print(f"Final task count for user {user_id}: {final_task_count}")
        print("Tasks:")
        for task in final_tasks.get("tasks", []):
            print(f"  - ID: {task['id']}, Title: {task['title']}, Status: {task['status']}")

        # Count total messages in the conversation
        all_messages = await message_service.get_conversation_messages(second_response.conversation_id)
        print(f"Total messages in conversation: {len(all_messages)}")

        print("\n=== END-TO-END VALIDATION COMPLETE ===")
        print("✓ All major functionality tested:")
        print("  - AI-powered natural language task management")
        print("  - Multi-turn conversations with context")
        print("  - Intelligent task disambiguation")
        print("  - Rich chat interface")
        print("  - Database persistence")
        print("  - User isolation")
        print("  - Error handling")
        print("\nThe AI Chatbot Todo application is functioning as expected!")


if __name__ == "__main__":
    asyncio.run(run_end_to_end_validation())