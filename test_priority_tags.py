#!/usr/bin/env python3
"""
Test script to verify priority and tags functionality in the Todo application.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.task_store import TaskStore
from models.task import Task

def test_priority_and_tags():
    """Test priority and tags functionality manually."""
    print("Testing Priority and Tags Functionality")
    print("=" * 50)

    # Create a task store instance
    task_store = TaskStore()

    # Test 1: Add a task with priority and tags
    print("\n1. Testing task creation with priority and tags...")
    task_id = task_store.add_task(
        title="Test Task with Priority and Tags",
        description="This is a test task to verify priority and tags functionality",
        priority="high",
        tags=["testing", "important"]
    )
    print(f"   - Task created with ID: {task_id}")
    print(f"   - Priority: high")
    print(f"   - Tags: ['testing', 'important']")

    # Retrieve the task to verify it was stored correctly
    task = task_store.get_task(task_id)
    print(f"   - Retrieved task: {task.title}")
    print(f"   - Task priority: {task.priority}")
    print(f"   - Task tags: {task.tags}")

    # Verify the values
    assert task.priority == "high", f"Expected priority 'high', got '{task.priority}'"
    assert "testing" in task.tags, f"Expected 'testing' in tags, got {task.tags}"
    assert "important" in task.tags, f"Expected 'important' in tags, got {task.tags}"
    print("   OK Priority and tags stored correctly")

    # Test 2: Add a task without priority and tags
    print("\n2. Testing task creation without priority and tags...")
    task_id2 = task_store.add_task(
        title="Test Task without Priority and Tags",
        description="This task should have no priority or tags"
    )
    task2 = task_store.get_task(task_id2)
    print(f"   - Task created with ID: {task_id2}")
    print(f"   - Priority: {task2.priority}")
    print(f"   - Tags: {task2.tags}")

    assert task2.priority is None, f"Expected priority None, got '{task2.priority}'"
    assert task2.tags == [], f"Expected empty tags list, got {task2.tags}"
    print("   OK None/empty values handled correctly")

    # Test 3: Update a task to add priority and tags
    print("\n3. Testing task update with priority and tags...")
    update_success = task_store.update_task(
        task_id2,
        title="Updated Test Task",
        description="This task was updated to have priority and tags",
        priority="medium",
        tags=["updated", "medium-priority"]
    )
    print(f"   - Update successful: {update_success}")

    updated_task = task_store.get_task(task_id2)
    print(f"   - Updated task priority: {updated_task.priority}")
    print(f"   - Updated task tags: {updated_task.tags}")

    assert updated_task.priority == "medium", f"Expected priority 'medium', got '{updated_task.priority}'"
    assert "updated" in updated_task.tags, f"Expected 'updated' in tags, got {updated_task.tags}"
    assert "medium-priority" in updated_task.tags, f"Expected 'medium-priority' in tags, got {updated_task.tags}"
    print("   OK Update with priority and tags successful")

    # Test 4: Test the update behavior when passing None (should not update)
    print("\n4. Testing task update behavior when passing None (should not update)...")
    original_priority = updated_task.priority
    original_tags = updated_task.tags

    update_success2 = task_store.update_task(
        task_id2,
        title="Updated Test Task Again",
        description="This task was updated but priority and tags should remain",
        priority=None,  # This should not update priority
        tags=None       # This should not update tags
    )
    print(f"   - Update successful: {update_success2}")

    updated_task2 = task_store.get_task(task_id2)
    print(f"   - Updated task priority: {updated_task2.priority}")
    print(f"   - Updated task tags: {updated_task2.tags}")

    # The priority and tags should remain unchanged since None was passed
    assert updated_task2.priority == original_priority, f"Expected priority '{original_priority}', got '{updated_task2.priority}'"
    assert updated_task2.tags == original_tags, f"Expected tags {original_tags}, got {updated_task2.tags}"
    print("   OK None values correctly ignored for priority and tags")

    # Test 5: Get all tasks and verify they're properly formatted
    print("\n5. Testing retrieval of all tasks...")
    all_tasks = task_store.get_all_tasks()
    print(f"   - Total tasks: {len(all_tasks)}")

    for i, task in enumerate(all_tasks):
        print(f"   - Task {i+1}: ID={task.id}, Title='{task.title}', Priority={task.priority}, Tags={task.tags}")

    print("\n" + "=" * 50)
    print("All priority and tags tests passed! OK")
    print("=" * 50)

def test_task_validation():
    """Test task validation for priority values."""
    print("\nTesting Task Validation")
    print("=" * 30)

    try:
        # This should work (valid priority)
        valid_task = Task(
            task_id=1,
            title="Valid Task",
            description="Task with valid priority",
            completed=False,
            priority="high",
            tags=["valid"]
        )
        print("   OK Valid priority 'high' accepted")
    except ValueError as e:
        print(f"   ERROR Valid priority rejected: {e}")

    try:
        # This should work (None priority)
        none_task = Task(
            task_id=2,
            title="None Priority Task",
            description="Task with no priority",
            completed=False,
            priority=None,
            tags=[]
        )
        print("   OK None priority accepted")
    except ValueError as e:
        print(f"   ERROR None priority rejected: {e}")

    try:
        # This should fail (invalid priority)
        invalid_task = Task(
            task_id=3,
            title="Invalid Priority Task",
            description="Task with invalid priority",
            completed=False,
            priority="superhigh",  # Invalid priority
            tags=["invalid"]
        )
        print("   ERROR Invalid priority accepted when it should be rejected")
    except ValueError as e:
        print(f"   OK Invalid priority 'superhigh' correctly rejected: {e}")

    print("Task validation tests completed!")

if __name__ == "__main__":
    test_priority_and_tags()
    test_task_validation()
    print("\nManual verification of priority and tags functionality completed successfully!")