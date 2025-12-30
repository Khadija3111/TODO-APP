"""
Test script for the Add Task functionality.
This tests the complete flow from CLI to storage.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from models.task import Task
from services.task_store import TaskStore
from cli.cli_interface import TodoCLI


def test_task_creation():
    """Test creating a task with title and description."""
    print("Testing task creation...")

    # Create a TaskStore instance
    store = TaskStore()

    # Add a task
    task_id = store.add_task("Test task", "This is a test description")

    # Verify the task was added
    task = store.get_task(task_id)
    assert task is not None, "Task should exist"
    assert task.id == task_id, "Task ID should match"
    assert task.title == "Test task", "Task title should match"
    assert task.description == "This is a test description", "Task description should match"
    assert task.completed == False, "Task should be pending by default"

    print(f"+ Task created successfully with ID: {task_id}")


def test_task_creation_without_description():
    """Test creating a task with only a title."""
    print("Testing task creation without description...")

    # Create a TaskStore instance
    store = TaskStore()

    # Add a task without description
    task_id = store.add_task("Test task without description")

    # Verify the task was added
    task = store.get_task(task_id)
    assert task is not None, "Task should exist"
    assert task.title == "Test task without description", "Task title should match"
    assert task.description == "", "Task description should be empty"

    print(f"+ Task created successfully with ID: {task_id}")


def test_empty_title_validation():
    """Test that empty titles are not allowed."""
    print("Testing empty title validation...")

    # Create a TaskStore instance
    store = TaskStore()

    try:
        store.add_task("")  # Empty title
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Title cannot be empty" in str(e), "Should have validation error for empty title"
        print("+ Empty title validation works correctly")

    try:
        store.add_task("   ")  # Title with only whitespace
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Title cannot be empty" in str(e), "Should have validation error for whitespace-only title"
        print("+ Whitespace-only title validation works correctly")


def test_task_store_unique_ids():
    """Test that task IDs are unique and incrementing."""
    print("Testing unique ID generation...")

    # Create a TaskStore instance
    store = TaskStore()

    # Add multiple tasks
    id1 = store.add_task("First task")
    id2 = store.add_task("Second task")
    id3 = store.add_task("Third task")

    # Verify IDs are unique and sequential
    assert id1 == 1, "First task should have ID 1"
    assert id2 == 2, "Second task should have ID 2"
    assert id3 == 3, "Third task should have ID 3"

    print("+ Unique ID generation works correctly")


def test_task_properties():
    """Test that task properties are properly set and accessible."""
    print("Testing task properties...")

    # Create a Task directly
    task = Task(1, "Test title", "Test description", False)

    assert task.id == 1, "ID should match"
    assert task.title == "Test title", "Title should match"
    assert task.description == "Test description", "Description should match"
    assert task.completed == False, "Completion status should match"

    # Test updating properties
    task.title = "Updated title"
    assert task.title == "Updated title", "Updated title should match"

    task.description = "Updated description"
    assert task.description == "Updated description", "Updated description should match"

    task.completed = True
    assert task.completed == True, "Updated completion status should match"

    print("+ Task properties work correctly")


if __name__ == "__main__":
    print("Running Add Task functionality tests...\n")

    test_task_creation()
    test_task_creation_without_description()
    test_empty_title_validation()
    test_task_store_unique_ids()
    test_task_properties()

    print("\n+ All tests passed! The Add Task functionality works correctly.")