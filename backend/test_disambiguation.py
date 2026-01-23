"""
Test script for task disambiguation functionality
This script tests the disambiguation logic in the chat agent
"""
import asyncio
from backend.agents.chat_agent import run_chat_agent
from backend.agents.task_resolver import resolve_task_by_reference, find_potential_task_matches, needs_clarification
from backend.mcp.tools.task_operations import add_task_tool, list_tasks_tool, ListTasksParams
from backend.models.task import Task
from uuid import uuid4


async def test_disambiguation_scenarios():
    """Test disambiguation scenarios with multiple similar tasks"""

    print("Testing disambiguation scenarios...")

    # Create a test user ID
    user_id = str(uuid4())

    # Add some test tasks with similar names
    print("\n1. Adding test tasks with similar names:")

    # Add tasks with similar titles for testing disambiguation
    await add_task_tool(type('AddTaskParams', (), {
        'user_id': user_id,
        'title': 'Buy groceries',
        'description': 'Go to the supermarket and buy food'
    })())

    await add_task_tool(type('AddTaskParams', (), {
        'user_id': user_id,
        'title': 'Buy groceries for dinner',
        'description': 'Buy ingredients for tonight\'s dinner'
    })())

    await add_task_tool(type('AddTaskParams', (), {
        'user_id': user_id,
        'title': 'Call mom',
        'description': 'Call mother for her birthday'
    })())

    await add_task_tool(type('AddTaskParams', (), {
        'user_id': user_id,
        'title': 'Call dad',
        'description': 'Call father about weekend plans'
    })())

    await add_task_tool(type('AddTaskParams', (), {
        'user_id': user_id,
        'title': 'Meeting with team',
        'description': 'Weekly team meeting at 10am'
    })())

    await add_task_tool(type('AddTaskParams', (), {
        'user_id': user_id,
        'title': 'Meeting with client',
        'description': 'Client presentation at 2pm'
    })())

    # List all tasks to verify they were created
    list_params = ListTasksParams(user_id=user_id, status="all")
    tasks_result = await list_tasks_tool(list_params)
    tasks = tasks_result.get("tasks", [])

    print(f"Created {len(tasks)} tasks:")
    for task in tasks:
        print(f"  - ID: {task['id']}, Title: {task['title']}")

    # Test 1: Test task resolution by exact name
    print("\n2. Testing task resolution by exact name:")
    resolved_task = await resolve_task_by_reference("Buy groceries", user_id, tasks)
    if resolved_task:
        print(f"✓ Resolved 'Buy groceries' to task ID {resolved_task['id']}: {resolved_task['title']}")
    else:
        print("✗ Failed to resolve 'Buy groceries'")

    # Test 2: Test finding potential matches for ambiguous reference
    print("\n3. Testing potential matches for ambiguous reference 'Buy groceries':")
    potential_matches = await find_potential_task_matches("Buy groceries", user_id)
    print(f"Found {len(potential_matches)} potential matches for 'Buy groceries':")
    for match in potential_matches:
        print(f"  - ID: {match['id']}, Title: {match['title']}, Status: {match['status']}")

    # Test 3: Test if clarification is needed for ambiguous reference
    print("\n4. Testing if clarification is needed for 'Buy groceries':")
    needs_clar = needs_clarification("Buy groceries", potential_matches)
    print(f"Clarification needed: {needs_clar}")

    # Test 4: Test finding potential matches for 'call' which should match multiple tasks
    print("\n5. Testing potential matches for ambiguous reference 'call':")
    call_matches = await find_potential_task_matches("call", user_id)
    print(f"Found {len(call_matches)} potential matches for 'call':")
    for match in call_matches:
        print(f"  - ID: {match['id']}, Title: {match['title']}, Status: {match['status']}")

    # Test 5: Test if clarification is needed for 'call' reference
    print("\n6. Testing if clarification is needed for 'call':")
    needs_clar = needs_clarification("call", call_matches)
    print(f"Clarification needed: {needs_clar}")

    # Test 6: Test finding potential matches for 'meeting' which should match multiple tasks
    print("\n7. Testing potential matches for ambiguous reference 'meeting':")
    meeting_matches = await find_potential_task_matches("meeting", user_id)
    print(f"Found {len(meeting_matches)} potential matches for 'meeting':")
    for match in meeting_matches:
        print(f"  - ID: {match['id']}, Title: {match['title']}, Status: {match['status']}")

    # Test 7: Test if clarification is needed for 'meeting' reference
    print("\n8. Testing if clarification is needed for 'meeting':")
    needs_clar = needs_clarification("meeting", meeting_matches)
    print(f"Clarification needed: {needs_clar}")

    # Test 8: Test chat agent with ambiguous reference
    print("\n9. Testing chat agent with ambiguous reference:")

    # Simulate a conversation with disambiguation
    conversation_history = []

    # First, list tasks to establish context
    agent_response = await run_chat_agent(
        user_id=user_id,
        user_message="What tasks do I have?",
        conversation_history=conversation_history
    )

    print(f"Agent response: {agent_response['response'][:100]}...")

    # Now try to complete an ambiguous task
    agent_response = await run_chat_agent(
        user_id=user_id,
        user_message="Complete the meeting task",
        conversation_history=conversation_history + [
            {"role": "user", "content": "What tasks do I have?"},
            {"role": "assistant", "content": agent_response['response']}
        ]
    )

    print(f"Agent response to 'Complete the meeting task': {agent_response['response'][:200]}...")

    # Test 9: Test with a unique task reference
    print("\n10. Testing chat agent with unique reference:")
    agent_response = await run_chat_agent(
        user_id=user_id,
        user_message="Complete the Meeting with team",
        conversation_history=conversation_history + [
            {"role": "user", "content": "What tasks do I have?"},
            {"role": "assistant", "content": "You have several tasks including 'Meeting with team', 'Meeting with client', 'Call mom', 'Call dad', 'Buy groceries', 'Buy groceries for dinner'"},
            {"role": "user", "content": "Complete the Meeting with team"},
            {"role": "assistant", "content": agent_response['response']}
        ]
    )

    print(f"Agent response to 'Complete the Meeting with team': {agent_response['response'][:200]}...")

    print("\nDisambiguation testing completed!")


if __name__ == "__main__":
    asyncio.run(test_disambiguation_scenarios())