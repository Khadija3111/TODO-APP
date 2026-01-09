#!/usr/bin/env python3
"""
Final integration test to verify all features work together.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from cli.cli_interface import TodoCLI
from services.task_store import TaskStore

def test_integration():
    """Test that all features work together correctly."""
    print("Final Integration Testing")
    print("=" * 30)

    # Create a task store for testing
    task_store = TaskStore()

    print("\n1. Testing task creation with all new features...")
    # Add a task with priority and tags
    task_id1 = task_store.add_task(
        title="Integration Test Task",
        description="This task tests all new features together",
        priority="high",
        tags=["integration", "test", "feature"]
    )
    print(f"   - Created task with ID: {task_id1}, priority: high, tags: ['integration', 'test', 'feature']")

    # Add another task
    task_id2 = task_store.add_task(
        title="Second Test Task",
        description="Another task for testing",
        priority="medium",
        tags=["test", "secondary"]
    )
    print(f"   - Created task with ID: {task_id2}, priority: medium, tags: ['test', 'secondary']")

    # Add a third task
    task_id3 = task_store.add_task(
        title="Low Priority Task",
        description="A low priority task",
        priority="low",
        tags=["low-priority"]
    )
    print(f"   - Created task with ID: {task_id3}, priority: low, tags: ['low-priority']")

    print("\n2. Testing search functionality...")
    search_results = task_store.search_tasks("integration")
    print(f"   - Search for 'integration' found {len(search_results)} task(s)")
    assert len(search_results) >= 1, "Search should find the integration task"

    search_results2 = task_store.search_tasks("test")
    print(f"   - Search for 'test' found {len(search_results2)} task(s)")
    assert len(search_results2) >= 2, "Search should find multiple test tasks"

    print("\n3. Testing filter functionality...")
    # Filter by priority
    high_priority_tasks = task_store.filter_tasks(priority="high")
    print(f"   - Filter by high priority found {len(high_priority_tasks)} task(s)")
    assert len(high_priority_tasks) == 1, "Should have 1 high priority task"

    # Filter by tags
    test_tag_tasks = task_store.filter_tasks(tags=["test"])
    print(f"   - Filter by 'test' tag found {len(test_tag_tasks)} task(s)")
    assert len(test_tag_tasks) >= 2, "Should have at least 2 tasks with 'test' tag"

    # Filter by status (all are pending by default)
    pending_tasks = task_store.filter_tasks(status="pending")
    print(f"   - Filter by pending status found {len(pending_tasks)} task(s)")
    assert len(pending_tasks) == 3, "Should have 3 pending tasks"

    print("\n4. Testing sort functionality...")
    # Sort by priority
    sorted_by_priority = task_store.sort_tasks(sort_field="priority", sort_order="asc")
    priorities = [task.priority for task in sorted_by_priority]
    print(f"   - Sorted by priority (asc): {priorities}")
    # Should be [low, medium, high] with None at end if present
    expected = ["low", "medium", "high"]
    non_none_priorities = [p for p in priorities if p is not None]
    assert non_none_priorities == sorted(non_none_priorities, key=lambda x: {"low": 1, "medium": 2, "high": 3}[x]), "Priorities should be sorted correctly"

    # Sort by alpha
    sorted_alpha = task_store.sort_tasks(sort_field="alpha", sort_order="asc")
    titles = [task.title for task in sorted_alpha]
    print(f"   - Sorted alphabetically (asc): {titles}")
    assert titles == sorted(titles, key=str.lower), "Titles should be sorted alphabetically"

    print("\n5. Testing update functionality...")
    # Update a task's priority and tags
    success = task_store.update_task(
        task_id2,
        title="Updated Test Task",
        description="Updated description",
        priority="high",  # Change priority from medium to high
        tags=["updated", "test"]  # Change tags
    )
    print(f"   - Updated task {task_id2} successfully: {success}")
    assert success, "Update should succeed"

    updated_task = task_store.get_task(task_id2)
    assert updated_task.priority == "high", "Priority should be updated to high"
    assert "updated" in updated_task.tags, "Tags should include 'updated'"
    print(f"   - Updated task has priority: {updated_task.priority}, tags: {updated_task.tags}")

    print("\n6. Testing toggle functionality...")
    # Toggle task completion
    toggle_success = task_store.toggle_task_completion(task_id1)
    print(f"   - Toggled completion for task {task_id1}: {toggle_success}")
    assert toggle_success, "Toggle should succeed"

    toggled_task = task_store.get_task(task_id1)
    assert toggled_task.completed == True, "Task should now be completed"
    print(f"   - Task {task_id1} is now completed: {toggled_task.completed}")

    print("\n7. Testing combined filters and sorts...")
    # Filter completed tasks and sort by priority
    completed_tasks = task_store.filter_tasks(status="completed")
    sorted_completed = task_store.sort_tasks(sort_field="priority", sort_order="desc")
    print(f"   - Found {len(completed_tasks)} completed tasks")
    print(f"   - All tasks sorted by priority (desc): {[t.priority for t in sorted_completed if t.priority]}")

    # Filter high priority tasks that contain "test" in title
    high_priority_tasks = task_store.filter_tasks(priority="high")
    test_in_title = [t for t in high_priority_tasks if "test" in t.title.lower()]
    print(f"   - High priority tasks with 'test' in title: {len(test_in_title)}")

    print("\n8. Testing CLI interface integration...")
    # Test CLI with color and without color
    cli_color = TodoCLI(use_color=True)
    cli_no_color = TodoCLI(use_color=False)
    print("   - Created CLI instances with and without color support")

    print("\n" + "=" * 30)
    print("All integration tests passed! OK")
    print("All features work correctly together!")
    print("=" * 30)

if __name__ == "__main__":
    test_integration()
    print("\nFinal integration testing completed successfully!")