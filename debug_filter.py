#!/usr/bin/env python3
"""
Debug script to check the filter functionality.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.task_store import TaskStore

def debug_filters():
    # Create a task store instance
    task_store = TaskStore()

    # Add tasks
    task_id1 = task_store.add_task(
        title="Complete project proposal",
        description="Finish the project proposal document",
        priority="high",
        tags=["work", "important"]
    )
    print(f"Added task 1: ID {task_id1}, title: 'Complete project proposal'")

    task_id2 = task_store.add_task(
        title="Buy groceries",
        description="Buy weekly groceries",
        priority="medium",
        tags=["personal", "shopping"]
    )
    print(f"Added task 2: ID {task_id2}, title: 'Buy groceries'")

    task_id3 = task_store.add_task(
        title="Read Python documentation",
        description="Read about new Python features",
        priority="low",
        tags=["learning", "python"]
    )
    print(f"Added task 3: ID {task_id3}, title: 'Read Python documentation'")

    task_id4 = task_store.add_task(
        title="Fix critical bug",
        description="Fix the critical bug in production",
        priority="high",
        tags=["urgent", "work", "bug"]
    )
    print(f"Added task 4: ID {task_id4}, title: 'Fix critical bug'")

    task_id5 = task_store.add_task(
        title="Review code changes",
        description="Review team's code changes",
        priority="medium",
        tags=["work", "review"]
    )
    print(f"Added task 5: ID {task_id5}, title: 'Review code changes'")

    # Toggle task 1 to completed
    task_store.toggle_task_completion(task_id1)
    print(f"Toggled task {task_id1} to completed")

    # Toggle task 5 to completed
    task_store.toggle_task_completion(task_id5)
    print(f"Toggled task {task_id5} to completed")

    # Check all tasks
    all_tasks = task_store.get_all_tasks()
    for task in all_tasks:
        print(f"Task ID {task.id}: '{task.title}', Status: {'Completed' if task.completed else 'Pending'}, Priority: {task.priority}")

    # Test completed filter
    completed_tasks = task_store.filter_tasks(status="completed")
    print(f"\nCompleted tasks: {len(completed_tasks)}")
    for task in completed_tasks:
        print(f"  - Task ID {task.id}: '{task.title}', Status: {'Completed' if task.completed else 'Pending'}, Priority: {task.priority}")

if __name__ == "__main__":
    debug_filters()