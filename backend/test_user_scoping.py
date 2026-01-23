"""
Test script for user_id scoping validation in MCP operations
This script tests that user_id scoping is properly enforced in all MCP operations
"""

import asyncio
import json
from backend.mcp.tools.task_operations import (
    add_task_tool, list_tasks_tool, complete_task_tool,
    delete_task_tool, update_task_tool
)
from backend.mcp.tools.task_operations import AddTaskParams, ListTasksParams, CompleteTaskParams, DeleteTaskParams, UpdateTaskParams
import uuid


async def test_user_id_scoping():
    """Test user_id scoping validation in MCP operations"""

    print("Testing user_id scoping validation...")

    # Create two different user IDs
    user_id_1 = str(uuid.uuid4())
    user_id_2 = str(uuid.uuid4())

    # Test 1: Add a task for user 1
    print("\n1. Adding task for user 1:")
    add_params_1 = AddTaskParams(
        user_id=user_id_1,
        title="Task for user 1",
        description="This task belongs to user 1",
    )
    add_result_1 = await add_task_tool(add_params_1)
    print(f"Add task for user 1 result: {add_result_1}")

    if not add_result_1.get("success"):
        print("ERROR: Failed to add task for user 1")
        return

    task_id_1 = add_result_1.get("task_id")
    if not task_id_1:
        print("ERROR: No task ID returned for user 1")
        return

    # Test 2: Add a task for user 2
    print("\n2. Adding task for user 2:")
    add_params_2 = AddTaskParams(
        user_id=user_id_2,
        title="Task for user 2",
        description="This task belongs to user 2",
    )
    add_result_2 = await add_task_tool(add_params_2)
    print(f"Add task for user 2 result: {add_result_2}")

    if not add_result_2.get("success"):
        print("ERROR: Failed to add task for user 2")
        return

    task_id_2 = add_result_2.get("task_id")
    if not task_id_2:
        print("ERROR: No task ID returned for user 2")
        return

    # Test 3: User 1 tries to list their tasks (should only see their own)
    print("\n3. User 1 listing their tasks:")
    list_params_1 = ListTasksParams(user_id=user_id_1, status="all")
    list_result_1 = await list_tasks_tool(list_params_1)
    print(f"User 1 tasks: {list_result_1}")
    user1_task_count = list_result_1.get("count", 0)
    print(f"User 1 has {user1_task_count} tasks")

    # Test 4: User 2 tries to list their tasks (should only see their own)
    print("\n4. User 2 listing their tasks:")
    list_params_2 = ListTasksParams(user_id=user_id_2, status="all")
    list_result_2 = await list_tasks_tool(list_params_2)
    print(f"User 2 tasks: {list_result_2}")
    user2_task_count = list_result_2.get("count", 0)
    print(f"User 2 has {user2_task_count} tasks")

    # Test 5: User 1 tries to access user 2's task (should fail)
    print("\n5. User 1 attempting to update user 2's task (should fail):")
    update_params_cross = UpdateTaskParams(
        user_id=user_id_1,
        task_id=task_id_2,  # User 1 trying to access user 2's task
        title="Attempt to modify other user's task"
    )
    update_result_cross = await update_task_tool(update_params_cross)
    print(f"Cross-user update result: {update_result_cross}")
    print(f"Success expected: False, Actual: {update_result_cross.get('success')}")

    # Test 6: User 2 tries to access user 1's task (should fail)
    print("\n6. User 2 attempting to complete user 1's task (should fail):")
    complete_params_cross = CompleteTaskParams(
        user_id=user_id_2,
        task_id=task_id_1,  # User 2 trying to access user 1's task
    )
    complete_result_cross = await complete_task_tool(complete_params_cross)
    print(f"Cross-user complete result: {complete_result_cross}")
    print(f"Success expected: False, Actual: {complete_result_cross.get('success')}")

    # Test 7: Test invalid user_id format
    print("\n7. Testing invalid user_id format:")
    invalid_user_id = "invalid-uuid-format"
    list_params_invalid = ListTasksParams(user_id=invalid_user_id, status="all")
    list_result_invalid = await list_tasks_tool(list_params_invalid)
    print(f"Invalid user_id result: {list_result_invalid}")
    print(f"Success expected: False, Actual: {list_result_invalid.get('success')}")

    # Clean up: Delete both tasks
    print("\n8. Cleaning up - deleting tasks:")
    delete_params_1 = DeleteTaskParams(user_id=user_id_1, task_id=task_id_1)
    delete_result_1 = await delete_task_tool(delete_params_1)
    print(f"Delete user 1's task: {delete_result_1}")

    delete_params_2 = DeleteTaskParams(user_id=user_id_2, task_id=task_id_2)
    delete_result_2 = await delete_task_tool(delete_params_2)
    print(f"Delete user 2's task: {delete_result_2}")

    print("\nUser_id scoping validation completed!")


if __name__ == "__main__":
    asyncio.run(test_user_id_scoping())