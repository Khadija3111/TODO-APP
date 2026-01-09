"""
Task Store Service

This module provides the in-memory storage and management for tasks.
"""

from typing import Dict, List, Optional
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from models.task import Task


class TaskStore:
    """
    In-memory task storage and management service.
    """

    def __init__(self):
        """
        Initialize the TaskStore with an empty collection of tasks and starting ID.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "") -> int:
        """
        Add a new task to the store with a unique ID.

        Args:
            title (str): The title of the task (required)
            description (str): The description of the task (optional)

        Returns:
            int: The ID of the newly created task

        Raises:
            ValueError: If title is empty or contains only whitespace
        """
        # Validate inputs
        if not isinstance(title, str):
            raise ValueError("Title must be a string")

        if not title.strip():
            raise ValueError("Title cannot be empty or contain only whitespace")

        if not isinstance(description, str):
            raise ValueError("Description must be a string")

        # Create a new task with the next available ID
        task = Task(
            task_id=self._next_id,
            title=title.strip(),
            description=description.strip(),
            completed=False
        )

        # Add the task to the store
        self._tasks[self._next_id] = task

        # Increment the next ID for the subsequent task
        task_id = self._next_id
        self._next_id += 1

        return task_id

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by its ID.

        Args:
            task_id (int): The ID of the task to retrieve

        Returns:
            Task: The task with the specified ID, or None if not found
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")

        return self._tasks.get(task_id)

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> bool:
        """
        Update an existing task's title or description.

        Args:
            task_id (int): The ID of the task to update
            title (str, optional): The new title for the task
            description (str, optional): The new description for the task

        Returns:
            bool: True if the task was updated successfully, False otherwise
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")

        task = self._tasks.get(task_id)
        if task is None:
            return False

        if title is not None:
            task.title = title

        if description is not None:
            task.description = description

        return True

    def delete_task(self, task_id: int) -> bool:
        """
        Remove a task by its ID.

        Args:
            task_id (int): The ID of the task to delete

        Returns:
            bool: True if the task was deleted successfully, False otherwise
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")

        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def toggle_task_completion(self, task_id: int) -> bool:
        """
        Change a task's completed status.

        Args:
            task_id (int): The ID of the task to toggle

        Returns:
            bool: True if the task status was toggled successfully, False otherwise
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")

        task = self._tasks.get(task_id)
        if task is None:
            return False

        task.completed = not task.completed
        return True

    def list_all_tasks(self) -> List[Task]:
        """
        Return all tasks in the store.

        Returns:
            List[Task]: A list of all tasks in the store
        """
        return list(self._tasks.values())

    def get_all_tasks(self) -> List[Task]:
        """
        Return all tasks in the store (alias for list_all_tasks).

        Returns:
            List[Task]: A list of all tasks in the store
        """
        return list(self._tasks.values())

    def get_next_id(self) -> int:
        """
        Get the next available task ID.

        Returns:
            int: The next available task ID
        """
        return self._next_id

    def clear_all_tasks(self) -> None:
        """
        Remove all tasks from the store.
        """
        self._tasks.clear()
        self._next_id = 1