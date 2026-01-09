#!/usr/bin/env python3
"""
Test specific filter combination: completed + high priority.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.task_store import TaskStore

def test_specific_filter():
    # Create a task store instance
    task_store = TaskStore()

    # Add the exact same tasks as in the test
    task_ids = []
    task_ids.append(task_store.add_task(
        title="Complete project proposal",
        description="Finish the project proposal document",
        priority="high",
        tags=["work", "important"]
    ))
    task_store.toggle_task_completion(task_ids[0])  # Task ID 1: completed, high priority

    task_ids.append(task_store.add_task(  # Task ID 2
        title="Buy groceries",
        description="Buy weekly groceries",
        priority="medium",
        tags=["personal", "shopping"]
    ))  # pending, medium priority

    task_ids.append(task_store.add_task(  # Task ID 3
        title="Read Python documentation",
        description="Read about new Python features",
        priority="low",
        tags=["learning", "python"]
    ))  # pending, low priority

    task_ids.append(task_store.add_task(  # Task ID 4
        title="Fix critical bug",
        description="Fix the critical bug in production",
        priority="high",
        tags=["urgent", "work", "bug"]
    ))  # pending, high priority

    task_ids.append(task_store.add_task(  # Task ID 5
        title="Review code changes",
        description="Review team's code changes",
        priority="medium",
        tags=["work", "review"]
    ))
    task_store.toggle_task_completion(task_ids[4])  # Task ID 5: completed, medium priority

    task_ids.append(task_store.add_task(  # Task ID 6
        title="Plan weekend trip",
        description="Plan the upcoming weekend trip",
        priority="low",
        tags=["personal", "trip"]
    ))  # pending, low priority

    # Test completed + high priority filter
    completed_high_tasks = task_store.filter_tasks(status="completed", priority="high")
    print(f"Completed high priority tasks: {len(completed_high_tasks)}")
    for task in completed_high_tasks:
        print(f"  - ID: {task.id}, Title: '{task.title}', Status: {'Completed' if task.completed else 'Pending'}, Priority: {task.priority}")

    # Should return only task ID 1
    expected_count = 1
    actual_count = len(completed_high_tasks)
    print(f"Expected: {expected_count}, Actual: {actual_count}")
    if actual_count == expected_count:
        print("Test PASSED")
    else:
        print("Test FAILED")

if __name__ == "__main__":
    test_specific_filter()