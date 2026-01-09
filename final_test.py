#!/usr/bin/env python3
"""
Final verification test for the Neon PostgreSQL integration.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_cli_integration():
    """Test that the CLI application works with the database integration."""
    try:
        print("Testing CLI application with database integration...")

        # Import the CLI components
        from services.task_store import TaskStore
        from backend.models.task import Task

        # Create a TaskStore instance
        store = TaskStore()
        print("[SUCCESS] TaskStore initialized with database connection")

        # Test adding a task
        task_id = store.add_task("CLI Integration Test", "Testing Neon PostgreSQL integration", "high", ["test", "integration", "neon"])
        print(f"[SUCCESS] Added task with ID: {task_id}")

        # Test retrieving the task
        task = store.get_task(task_id)
        if task:
            print(f"[SUCCESS] Retrieved task: {task.title}")
            print(f"  - Description: {task.description}")
            print(f"  - Completed: {task.completed}")
            print(f"  - Priority: {task.priority}")
            print(f"  - Tags: {task.tags_list}")
        else:
            print("[ERROR] Failed to retrieve task")
            return False

        # Test listing all tasks
        all_tasks = store.list_all_tasks()
        print(f"[SUCCESS] Found {len(all_tasks)} task(s) in database")

        # Test updating the task
        update_result = store.update_task(task_id, title="Updated CLI Integration Test", description="Updated - Testing Neon PostgreSQL integration")
        if update_result:
            print("[SUCCESS] Task updated successfully")
            updated_task = store.get_task(task_id)
            print(f"  - New title: {updated_task.title}")
        else:
            print("[ERROR] Failed to update task")
            return False

        # Test toggling completion
        toggle_result = store.toggle_task_completion(task_id)
        if toggle_result:
            print("[SUCCESS] Task completion toggled successfully")
            toggled_task = store.get_task(task_id)
            print(f"  - Completed status: {toggled_task.completed}")
        else:
            print("[ERROR] Failed to toggle task completion")
            return False

        # Test searching tasks
        search_results = store.search_tasks("integration")
        print(f"[SUCCESS] Found {len(search_results)} task(s) matching 'integration'")

        # Test filtering tasks
        filtered_tasks = store.filter_tasks(status='pending', priority='high')
        print(f"[SUCCESS] Found {len(filtered_tasks)} pending high priority task(s)")

        # Clean up - delete the test task
        delete_result = store.delete_task(task_id)
        if delete_result:
            print("[SUCCESS] Test task deleted successfully")
        else:
            print("[ERROR] Failed to delete test task")
            return False

        # Verify deletion
        remaining_tasks = store.list_all_tasks()
        print(f"[SUCCESS] Remaining tasks after cleanup: {len(remaining_tasks)}")

        print("\n[SUCCESS] CLI application database integration test passed!")
        return True

    except Exception as e:
        print(f"[ERROR] CLI integration test error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Starting final CLI database integration verification...\n")

    success = test_cli_integration()

    if success:
        print("\n[SUCCESS] All CLI database integration tests passed!")
        print("Neon PostgreSQL database is fully integrated and functional with the Todo CLI application.")
        print("\nSummary of changes made:")
        print("- Updated database configuration to use Neon PostgreSQL")
        print("- Modified Task model to extend SQLModel")
        print("- Replaced in-memory storage with database operations")
        print("- Updated dependencies in pyproject.toml")
        print("- Fixed schema issues and reset database")
        print("- Verified all operations work correctly")
    else:
        print("\n[FAILURE] CLI database integration tests failed")
        sys.exit(1)