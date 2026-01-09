#!/usr/bin/env python3
"""
Debug script to check the search functionality.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.task_store import TaskStore

def debug_search():
    # Create a task store instance
    task_store = TaskStore()

    # Add a task with 'grocery' in description
    task_id = task_store.add_task(
        title="Buy groceries",
        description="Need to buy groceries for the week including milk, bread, eggs",
        priority="medium",
        tags=["shopping", "personal"]
    )

    print(f"Task ID: {task_id}")
    task = task_store.get_task(task_id)
    print(f"Task title: '{task.title}'")
    print(f"Task description: '{task.description}'")
    print(f"'grocery' in title: {'grocery' in task.title.lower()}")
    print(f"'grocery' in description: {'grocery' in task.description.lower()}")
    print(f"'grocer' in title: {'grocer' in task.title.lower()}")
    print(f"'grocer' in description: {'grocer' in task.description.lower()}")
    print(f"'buy' in title: {'buy' in task.title.lower()}")
    print(f"'buy' in description: {'buy' in task.description.lower()}")

    # Try searching
    results = task_store.search_tasks("grocery")
    print(f"Search results for 'grocery': {len(results)} tasks")
    for result in results:
        print(f"  - Found task: '{result.title}' - '{result.description}'")

if __name__ == "__main__":
    debug_search()