#!/usr/bin/env python3
"""
Test script to verify Neon PostgreSQL database integration with the Todo application.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.task_store import TaskStore

def test_database_connection():
    """Test the database connection and basic task operations."""
    print("Testing database connection and task operations...")

    try:
        # Create a task store instance
        store = TaskStore()
        print("✓ TaskStore initialized successfully")

        # Test adding a task
        task_id = store.add_task("Test Task", "This is a test task", "high", ["test", "important"])
        print(f"✓ Added task with ID: {task_id}")

        # Test retrieving the task
        task = store.get_task(task_id)
        if task:
            print(f"✓ Retrieved task: {task.title}")
            print(f"  - Description: {task.description}")
            print(f"  - Completed: {task.completed}")
            print(f"  - Priority: {task.priority}")
            print(f"  - Tags: {task.tags_list}")
        else:
            print("✗ Failed to retrieve task")

        # Test listing all tasks
        all_tasks = store.list_all_tasks()
        print(f"✓ Found {len(all_tasks)} task(s) in database")

        # Test updating the task
        update_result = store.update_task(task_id, title="Updated Test Task", description="Updated description")
        if update_result:
            print("✓ Task updated successfully")
            updated_task = store.get_task(task_id)
            print(f"  - New title: {updated_task.title}")
        else:
            print("✗ Failed to update task")

        # Test toggling completion
        toggle_result = store.toggle_task_completion(task_id)
        if toggle_result:
            print("✓ Task completion toggled successfully")
            toggled_task = store.get_task(task_id)
            print(f"  - Completed status: {toggled_task.completed}")
        else:
            print("✗ Failed to toggle task completion")

        # Test filtering tasks
        filtered_tasks = store.filter_tasks(status='all', priority='high')
        print(f"✓ Found {len(filtered_tasks)} high priority task(s)")

        # Test searching tasks
        search_results = store.search_tasks("test")
        print(f"✓ Found {len(search_results)} task(s) matching 'test'")

        # Clean up - delete the test task
        delete_result = store.delete_task(task_id)
        if delete_result:
            print("✓ Test task deleted successfully")
        else:
            print("✗ Failed to delete test task")

        # Verify deletion
        remaining_tasks = store.list_all_tasks()
        print(f"✓ Remaining tasks after cleanup: {len(remaining_tasks)}")

        print("\n✓ All database integration tests passed!")
        return True

    except Exception as e:
        print(f"\n✗ Error during database testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_database_connection()
    if not success:
        sys.exit(1)
    else:
        print("\nDatabase integration verified successfully!")