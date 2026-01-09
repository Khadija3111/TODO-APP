#!/usr/bin/env python3
"""
Test script to verify search functionality in the Todo application.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.task_store import TaskStore

def test_search_functionality():
    """Test search functionality with various keywords and scenarios."""
    print("Testing Search Functionality")
    print("=" * 40)

    # Create a task store instance
    task_store = TaskStore()

    # Add some test tasks with different content
    print("\n1. Adding test tasks...")
    task_ids = []

    # Task with title containing 'meeting'
    task_ids.append(task_store.add_task(
        title="Team Meeting",
        description="Weekly team sync meeting to discuss project progress",
        priority="high",
        tags=["work", "meeting"]
    ))
    print(f"   - Added task: 'Team Meeting'")

    # Task with description containing 'grocery'
    task_ids.append(task_store.add_task(
        title="Buy groceries",
        description="Need to buy groceries for the week including milk, bread, eggs",
        priority="medium",
        tags=["shopping", "personal"]
    ))
    print(f"   - Added task: 'Buy groceries'")

    # Task with tags containing 'urgent'
    task_ids.append(task_store.add_task(
        title="Fix critical bug",
        description="Fix the critical bug in the payment processing system",
        priority="high",
        tags=["urgent", "work", "bug"]
    ))
    print(f"   - Added task: 'Fix critical bug'")

    # Task with low priority
    task_ids.append(task_store.add_task(
        title="Read documentation",
        description="Read the new API documentation for future reference",
        priority="low",
        tags=["learning", "documentation"]
    ))
    print(f"   - Added task: 'Read documentation'")

    # Test 2: Search for 'meeting'
    print("\n2. Testing search for 'meeting'...")
    results = task_store.search_tasks("meeting")
    print(f"   - Found {len(results)} task(s) matching 'meeting'")
    for task in results:
        print(f"   - ID: {task.id}, Title: '{task.title}', Description: '{task.description}'")

    # Should find the 'Team Meeting' task
    assert len(results) >= 1, f"Expected at least 1 result for 'meeting', got {len(results)}"
    meeting_found = any("meeting" in task.title.lower() or "meeting" in task.description.lower() for task in results)
    assert meeting_found, "Expected to find task containing 'meeting'"
    print("   OK Found task containing 'meeting'")

    # Test 3: Search for 'grocer' (substring of 'groceries')
    print("\n3. Testing search for 'grocer' (substring of 'groceries')...")
    results = task_store.search_tasks("grocer")
    print(f"   - Found {len(results)} task(s) matching 'grocer'")
    for task in results:
        print(f"   - ID: {task.id}, Title: '{task.title}', Description: '{task.description}'")

    # Should find the 'Buy groceries' task (contains 'grocer' in 'groceries')
    assert len(results) >= 1, f"Expected at least 1 result for 'grocer', got {len(results)}"
    grocer_found = any("grocer" in task.title.lower() or "grocer" in task.description.lower() for task in results)
    assert grocer_found, "Expected to find task containing 'grocer' as substring"
    print("   OK Found task containing 'grocer' as substring")

    # Test 4: Search for 'urgent'
    print("\n4. Testing search for 'urgent'...")
    results = task_store.search_tasks("urgent")
    print(f"   - Found {len(results)} task(s) matching 'urgent'")
    for task in results:
        print(f"   - ID: {task.id}, Title: '{task.title}', Description: '{task.description}', Tags: {task.tags}")

    # Should find the 'Fix critical bug' task (has 'urgent' tag)
    assert len(results) >= 1, f"Expected at least 1 result for 'urgent', got {len(results)}"
    urgent_found = any("urgent" in task.tags for task in results)
    assert urgent_found, "Expected to find task with 'urgent' tag"
    print("   OK Found task with 'urgent' tag")

    # Test 5: Search for 'documentation'
    print("\n5. Testing search for 'documentation'...")
    results = task_store.search_tasks("documentation")
    print(f"   - Found {len(results)} task(s) matching 'documentation'")
    for task in results:
        print(f"   - ID: {task.id}, Title: '{task.title}', Description: '{task.description}'")

    # Should find the 'Read documentation' task
    assert len(results) >= 1, f"Expected at least 1 result for 'documentation', got {len(results)}"
    doc_found = any("documentation" in task.title.lower() or "documentation" in task.description.lower() for task in results)
    assert doc_found, "Expected to find task containing 'documentation'"
    print("   OK Found task containing 'documentation'")

    # Test 6: Case-insensitive search
    print("\n6. Testing case-insensitive search...")
    results = task_store.search_tasks("MEETING")  # Upper case
    print(f"   - Found {len(results)} task(s) matching 'MEETING' (upper case)")

    results_lower = task_store.search_tasks("meeting")  # Lower case
    print(f"   - Found {len(results_lower)} task(s) matching 'meeting' (lower case)")

    assert len(results) == len(results_lower), f"Case insensitive search failed: {len(results)} != {len(results_lower)}"
    print("   OK Case-insensitive search works correctly")

    # Test 7: Partial matching
    print("\n7. Testing partial matching...")
    results = task_store.search_tasks("meet")  # Partial of 'meeting'
    print(f"   - Found {len(results)} task(s) matching 'meet' (partial of 'meeting')")

    assert len(results) >= 1, f"Expected at least 1 result for partial match 'meet', got {len(results)}"
    print("   OK Partial matching works correctly")

    # Test 8: No results for non-existent keyword
    print("\n8. Testing search for non-existent keyword...")
    results = task_store.search_tasks("nonexistentkeyword")
    print(f"   - Found {len(results)} task(s) matching 'nonexistentkeyword'")

    assert len(results) == 0, f"Expected 0 results for 'nonexistentkeyword', got {len(results)}"
    print("   OK No results found for non-existent keyword")

    # Test 9: Search with special characters
    print("\n9. Testing search with special characters...")
    task_ids.append(task_store.add_task(
        title="Review API docs (v2)",
        description="Review the new API documentation for version 2",
        priority="medium",
        tags=["api", "docs"]
    ))
    print(f"   - Added task with special characters: 'Review API docs (v2)'")

    results = task_store.search_tasks("v2")
    print(f"   - Found {len(results)} task(s) matching 'v2'")
    assert len(results) >= 1, f"Expected at least 1 result for 'v2', got {len(results)}"
    print("   OK Search with special characters works correctly")

    print("\n" + "=" * 40)
    print("All search functionality tests passed! OK")
    print("=" * 40)

def test_search_meet_to_meeting():
    """Verify that 'todo search meet' returns tasks containing 'meeting'."""
    print("\nVerifying 'meet' search returns 'meeting' containing tasks")
    print("=" * 55)

    # Create a task store instance
    task_store = TaskStore()

    # Add a task with 'meeting' in the title
    task_id = task_store.add_task(
        title="Team meeting tomorrow",
        description="Prepare agenda for the team meeting",
        priority="high",
        tags=["work"]
    )
    print(f"   - Added task with 'meeting' in title: 'Team meeting tomorrow'")

    # Add another task with 'meeting' in the description
    task_id2 = task_store.add_task(
        title="Schedule call",
        description="Need to schedule a meeting with the client next week",
        priority="medium",
        tags=["call"]
    )
    print(f"   - Added task with 'meeting' in description: 'Schedule call'")

    # Search for 'meet' (partial match of 'meeting')
    results = task_store.search_tasks("meet")
    print(f"   - Search for 'meet' returned {len(results)} task(s)")

    # Check if both tasks were found
    found_task_ids = [task.id for task in results]
    print(f"   - Found task IDs: {found_task_ids}")

    assert task_id in found_task_ids, f"Task {task_id} with 'meeting' in title was not found by 'meet' search"
    assert task_id2 in found_task_ids, f"Task {task_id2} with 'meeting' in description was not found by 'meet' search"

    print("   OK Search for 'meet' correctly found tasks containing 'meeting'")
    print("Verification completed successfully!")

if __name__ == "__main__":
    test_search_functionality()
    test_search_meet_to_meeting()
    print("\nManual verification of search functionality completed successfully!")