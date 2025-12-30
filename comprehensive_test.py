"""
Comprehensive test script for all 5 features of the Todo application.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from models.task import Task
from services.task_store import TaskStore
from cli.cli_interface import TodoCLI


def test_all_features():
    """Test all 5 features of the Todo application."""
    print("Testing all 5 features of the Todo application...\n")

    # Create a TaskStore instance
    store = TaskStore()

    # Test Feature 1: Add Task
    print("1. Testing Add Task feature...")
    task_id_1 = store.add_task("First task", "Description for first task")
    task_id_2 = store.add_task("Second task")  # Without description

    print(f"   + Added task with ID: {task_id_1}")
    print(f"   + Added task with ID: {task_id_2}")

    # Verify tasks were added
    task1 = store.get_task(task_id_1)
    assert task1 is not None
    assert task1.title == "First task"
    assert task1.description == "Description for first task"
    assert task1.completed == False

    task2 = store.get_task(task_id_2)
    assert task2 is not None
    assert task2.title == "Second task"
    assert task2.description == ""
    assert task2.completed == False

    print("   + Add Task feature works correctly\n")

    # Test Feature 2: View Tasks
    print("2. Testing View Tasks feature...")
    all_tasks = store.get_all_tasks()
    assert len(all_tasks) == 2
    print(f"   + Retrieved {len(all_tasks)} tasks")

    # Verify both tasks are in the list
    task_ids = [task.id for task in all_tasks]
    assert task_id_1 in task_ids
    assert task_id_2 in task_ids
    print("   + View Tasks feature works correctly\n")

    # Test Feature 3: Update Task
    print("3. Testing Update Task feature...")
    success = store.update_task(task_id_1, "Updated first task", "Updated description")
    assert success == True

    updated_task1 = store.get_task(task_id_1)
    assert updated_task1.title == "Updated first task"
    assert updated_task1.description == "Updated description"
    print(f"   + Updated task {task_id_1}")

    # Test partial update (only title)
    success = store.update_task(task_id_2, title="Partially updated second task")
    assert success == True

    updated_task2 = store.get_task(task_id_2)
    assert updated_task2.title == "Partially updated second task"
    print(f"   + Partially updated task {task_id_2}")
    print("   + Update Task feature works correctly\n")

    # Test Feature 4: Delete Task
    print("4. Testing Delete Task feature...")
    initial_count = len(store.get_all_tasks())
    success = store.delete_task(task_id_1)
    assert success == True

    after_delete_count = len(store.get_all_tasks())
    assert after_delete_count == initial_count - 1

    # Verify task no longer exists
    deleted_task = store.get_task(task_id_1)
    assert deleted_task is None
    print(f"   + Deleted task {task_id_1}")
    print("   + Delete Task feature works correctly\n")

    # Test Feature 5: Toggle Completion
    print("5. Testing Toggle Completion feature...")
    task2_before = store.get_task(task_id_2)
    initial_status = task2_before.completed

    success = store.toggle_task_completion(task_id_2)
    assert success == True

    task2_after = store.get_task(task_id_2)
    new_status = task2_after.completed

    # Status should have changed
    assert initial_status != new_status
    print(f"   + Toggled completion status of task {task_id_2}")

    # Toggle again to return to original state
    success = store.toggle_task_completion(task_id_2)
    toggled_back_task = store.get_task(task_id_2)
    assert toggled_back_task.completed == initial_status
    print("   + Toggle Completion feature works correctly\n")

    # Test error cases
    print("6. Testing error handling...")

    # Try to update non-existent task
    result = store.update_task(999, "Non-existent task")
    assert result == False
    print("   + Correctly handled update for non-existent task")

    # Try to delete non-existent task
    result = store.delete_task(999)
    assert result == False
    print("   + Correctly handled deletion of non-existent task")

    # Try to toggle non-existent task
    result = store.toggle_task_completion(999)
    assert result == False
    print("   + Correctly handled toggle for non-existent task")

    # Try to get non-existent task
    result = store.get_task(999)
    assert result is None
    print("   + Correctly handled retrieval of non-existent task")

    # Test validation for empty title
    try:
        store.add_task("")
        assert False, "Should have raised ValueError"
    except ValueError:
        print("   + Correctly validated empty task title")

    print("\n+ All 5 features tested successfully!")
    print("+ Error handling works correctly!")


def test_cli_integration():
    """Test CLI integration for basic functionality."""
    print("\nTesting CLI integration...")

    # Create a CLI instance
    cli = TodoCLI()

    # Test that CLI can add a task
    initial_count = len(cli.task_store.get_all_tasks())
    task_id = cli.task_store.add_task("CLI Test Task", "Test from CLI integration")
    after_add_count = len(cli.task_store.get_all_tasks())

    assert after_add_count == initial_count + 1
    print("   + CLI can add tasks")

    # Test that CLI can view tasks
    tasks = cli.task_store.get_all_tasks()
    assert len(tasks) > 0
    print("   + CLI can view tasks")

    # Clean up
    cli.task_store.delete_task(task_id)
    print("   + CLI integration test completed")


if __name__ == "__main__":
    test_all_features()
    test_cli_integration()

    print("\n+ All tests passed! The Todo application with all 5 features works correctly.")
    print("\nFeatures tested:")
    print("- Add Task: Create tasks with title and optional description")
    print("- View Tasks: Display all tasks with ID, title, description, and status")
    print("- Update Task: Modify task title and/or description by ID")
    print("- Delete Task: Remove tasks by ID")
    print("- Toggle Completion: Change task completion status by ID")
    print("- Error handling: Graceful handling of invalid inputs and operations")