"""
Test script for MCP tools
This script tests the basic functionality of the MCP tools
"""

import asyncio
import json
from backend.mcp.server import mcp_server
from backend.models.user import User
from backend.models.task import Task
from backend.services.task_service import TaskService
from backend.utils.database import get_session
from sqlmodel import select
import uuid


async def test_mcp_tools():
    """Test basic MCP tools functionality"""

    # Initialize the MCP server
    server = mcp_server

    print("Testing MCP tools...")

    # Create a test user
    user_id = uuid.uuid4()

    # Test add_task tool
    print("\n1. Testing add_task tool:")
    add_task_params = {
        "user_id": str(user_id),
        "title": "Test task from MCP",
        "description": "This is a test task created via MCP",
        "priority": "medium",
        "category": "test"
    }

    # Simulate calling the add_task function directly
    from backend.mcp.tools.task_operations import add_task
    result = await add_task(**add_task_params)
    print(f"Add task result: {result}")

    # Test list_tasks tool
    print("\n2. Testing list_tasks tool:")
    list_params = {"user_id": str(user_id)}

    from backend.mcp.tools.task_operations import list_tasks
    result = await list_tasks(**list_params)
    print(f"List tasks result: {result}")

    # Test complete_task tool
    print("\n3. Testing complete_task tool:")
    if result and len(result) > 0:
        task_id = result[0]['id']
        complete_params = {
            "task_id": task_id,
            "user_id": str(user_id),
            "completed": True
        }

        from backend.mcp.tools.task_operations import complete_task
        result = await complete_task(**complete_params)
        print(f"Complete task result: {result}")

    # Test update_task tool
    print("\n4. Testing update_task tool:")
    if result and 'id' in result:
        update_params = {
            "task_id": result['id'],
            "user_id": str(user_id),
            "title": "Updated test task",
            "description": "This task has been updated via MCP",
            "priority": "high"
        }

        from backend.mcp.tools.task_operations import update_task
        update_result = await update_task(**update_params)
        print(f"Update task result: {update_result}")

    # Test delete_task tool
    print("\n5. Testing delete_task tool:")
    if result and 'id' in result:
        delete_params = {
            "task_id": result['id'],
            "user_id": str(user_id)
        }

        from backend.mcp.tools.task_operations import delete_task
        delete_result = await delete_task(**delete_params)
        print(f"Delete task result: {delete_result}")

    print("\nMCP tools testing completed!")


if __name__ == "__main__":
    asyncio.run(test_mcp_tools())