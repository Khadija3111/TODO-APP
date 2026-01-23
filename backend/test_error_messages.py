"""
Test script for validating error message clarity
This script tests various failure cases and verifies that error messages are user-friendly
"""
import asyncio
from backend.agents.chat_agent import run_chat_agent
from backend.mcp.tools.task_operations import (
    add_task_tool, list_tasks_tool, complete_task_tool,
    delete_task_tool, update_task_tool
)
from backend.mcp.tools.task_operations import AddTaskParams, ListTasksParams, CompleteTaskParams, DeleteTaskParams, UpdateTaskParams
from uuid import uuid4


async def test_error_message_clarity():
    """Test error message clarity for various failure cases"""

    print("Testing error message clarity...")

    # Create a test user ID
    user_id = str(uuid4())

    print("\n1. Testing error message for non-existent task completion:")

    # Try to complete a non-existent task
    result = await complete_task_tool(CompleteTaskParams(
        user_id=user_id,
        task_id="999999"
    ))

    print(f"Complete non-existent task result: {result}")
    if not result.get("success"):
        print(f"Error message: {result.get('message', 'No message')}")
        if "couldn't find a task with ID 999999" in result.get('message', ''):
            print("✓ Error message is clear and helpful")
        else:
            print("✗ Error message could be clearer")

    print("\n2. Testing error message for non-existent task deletion:")

    # Try to delete a non-existent task
    result = await delete_task_tool(DeleteTaskParams(
        user_id=user_id,
        task_id="999998"
    ))

    print(f"Delete non-existent task result: {result}")
    if not result.get("success"):
        print(f"Error message: {result.get('message', 'No message')}")
        if "couldn't find a task with ID 999998" in result.get('message', ''):
            print("✓ Error message is clear and helpful")
        else:
            print("✗ Error message could be clearer")

    print("\n3. Testing error message for non-existent task update:")

    # Try to update a non-existent task
    result = await update_task_tool(UpdateTaskParams(
        user_id=user_id,
        task_id="999997",
        title="Updated title"
    ))

    print(f"Update non-existent task result: {result}")
    if not result.get("success"):
        print(f"Error message: {result.get('message', 'No message')}")
        if "couldn't find a task with ID 999997" in result.get('message', ''):
            print("✓ Error message is clear and helpful")
        else:
            print("✗ Error message could be clearer")

    print("\n4. Testing error message for invalid user_id:")

    # Create another user ID and try to access tasks from a different user
    other_user_id = str(uuid4())

    # Add a task for the original user
    add_result = await add_task_tool(AddTaskParams(
        user_id=user_id,
        title="Original user task",
        description="Task for original user"
    ))

    if add_result.get("success"):
        task_id = add_result["task"]["id"]
        print(f"Added task with ID: {task_id} for user {user_id}")

        # Try to access that task from a different user (should fail due to user scoping)
        result = await list_tasks_tool(ListTasksParams(
            user_id=other_user_id,
            status="all"
        ))

        print(f"Other user tasks result: {result}")
        other_user_tasks = result.get("tasks", [])
        original_user_tasks = []

        # Check if the original user's task appears in other user's list (it shouldn't)
        for task in other_user_tasks:
            if str(task.get("id")) == str(task_id):
                print("✗ User scoping is not working properly - other user can see original user's task")
                break
        else:
            print("✓ User scoping is working - other user cannot see original user's task")

    print("\n5. Testing chat agent error responses:")

    # Test chat agent with non-existent task reference
    conversation_history = []

    agent_response = await run_chat_agent(
        user_id=user_id,
        user_message="Complete task 999996",
        conversation_history=conversation_history
    )

    print(f"Chat agent response for non-existent task: {agent_response['response']}")
    if "couldn't find a task with ID 999996" in agent_response['response']:
        print("✓ Chat agent provides clear error message for non-existent task")
    else:
        print("✗ Chat agent error message could be clearer")

    print("\n6. Testing chat agent with ambiguous task reference:")

    # Add a few tasks for disambiguation testing
    await add_task_tool(AddTaskParams(
        user_id=user_id,
        title="Meeting with John",
        description="Team meeting with John"
    ))

    await add_task_tool(AddTaskParams(
        user_id=user_id,
        title="Meeting with Jane",
        description="Project meeting with Jane"
    ))

    agent_response = await run_chat_agent(
        user_id=user_id,
        user_message="Complete the meeting task",
        conversation_history=conversation_history
    )

    print(f"Chat agent response for ambiguous task: {agent_response['response'][:200]}...")
    if "multiple tasks matching" in agent_response['response'] or "specify which one" in agent_response['response']:
        print("✓ Chat agent provides clear guidance for ambiguous task reference")
    else:
        print("✗ Chat agent should provide clearer guidance for ambiguous references")

    print("\n7. Testing malformed input handling:")

    # Test with empty or malformed inputs
    try:
        agent_response = await run_chat_agent(
            user_id=user_id,
            user_message="",
            conversation_history=[]
        )
        print(f"Empty message response: {agent_response['response'][:100]}...")
    except Exception as e:
        print(f"Error handling empty message: {str(e)}")

    print("\nError message clarity testing completed!")


if __name__ == "__main__":
    asyncio.run(test_error_message_clarity())