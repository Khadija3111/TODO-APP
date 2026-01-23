"""
Test script for MCP tools with database operations
This script tests the MCP tools directly with database operations
"""

import asyncio
import json
from backend.mcp.tools.task_operations import (
    add_task_tool, list_tasks_tool, complete_task_tool,
    delete_task_tool, update_task_tool
)
from backend.mcp.tools.task_operations import AddTaskParams, ListTasksParams, CompleteTaskParams, DeleteTaskParams, UpdateTaskParams
from backend.models.user import User
from backend.models.task import Task
from backend.services.task_service import TaskService
from backend.utils.database import get_session
from sqlmodel import select
import uuid


async def test_mcp_tools_database():
    """Test MCP tools directly with database operations"""

    print("Testing MCP tools with database operations...")

    # Create a test user ID
    user_id = str(uuid.uuid4())

    # Test 1: Add a task
    print("\n1. Testing add_task tool with database:")
    add_params = AddTaskParams(
        user_id=user_id,
        title="Test task from MCP database test",
        description="This is a test task created via MCP for database testing",
    )
    add_result = await add_task_tool(add_params)
    print(f"Add task result: {add_result}")

    if not add_result.get("success"):
        print("ERROR: Failed to add task")
        return

    task_id = add_result.get("task_id")
    if not task_id:
        print("ERROR: No task ID returned from add operation")
        return

    # Test 2: List tasks
    print("\n2. Testing list_tasks tool with database:")
    list_params = ListTasksParams(user_id=user_id, status="all")
    list_result = await list_tasks_tool(list_params)
    print(f"List tasks result: {list_result}")

    # Test 3: Update the task
    print("\n3. Testing update_task tool with database:")
    update_params = UpdateTaskParams(
        user_id=user_id,
        task_id=task_id,
        title="Updated test task from MCP",
        description="This task has been updated via MCP database test"
    )
    update_result = await update_task_tool(update_params)
    print(f"Update task result: {update_result}")

    # Test 4: Complete the task
    print("\n4. Testing complete_task tool with database:")
    complete_params = CompleteTaskParams(
        user_id=user_id,
        task_id=task_id
    )
    complete_result = await complete_task_tool(complete_params)
    print(f"Complete task result: {complete_result}")

    # Test 5: List tasks again to see the completed task
    print("\n5. Testing list_tasks tool again after completion:")
    list_result_after = await list_tasks_tool(list_params)
    print(f"List tasks result after completion: {list_result_after}")

    # Test 6: Delete the task
    print("\n6. Testing delete_task tool with database:")
    delete_params = DeleteTaskParams(
        user_id=user_id,
        task_id=task_id
    )
    delete_result = await delete_task_tool(delete_params)
    print(f"Delete task result: {delete_result}")

    # Test 7: List tasks again to confirm deletion
    print("\n7. Testing list_tasks tool after deletion:")
    list_result_final = await list_tasks_tool(list_params)
    print(f"List tasks result after deletion: {list_result_final}")

    print("\nMCP tools database testing completed!")


if __name__ == "__main__":
    asyncio.run(test_mcp_tools_database())