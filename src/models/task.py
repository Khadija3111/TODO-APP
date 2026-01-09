"""
Task Model

This module defines the Task data model for the todo application.
"""

from typing import Optional


class Task:
    """
    Represents a single todo task with id, title, description, and completion status.
    """

    def __init__(self, task_id: int, title: str, description: str = "", completed: bool = False):
        """
        Initialize a Task instance.

        Args:
            task_id (int): Unique identifier for the task
            title (str): Title of the task (required)
            description (str): Description of the task (optional)
            completed (bool): Completion status of the task (default: False)
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")

        if not isinstance(title, str):
            raise ValueError("Title must be a string")

        if not title.strip():
            raise ValueError("Title cannot be empty or contain only whitespace")

        if not isinstance(description, str):
            raise ValueError("Description must be a string")

        if not isinstance(completed, bool):
            raise ValueError("Completed status must be a boolean")

        self._id = task_id
        self._title = title.strip()
        self._description = description.strip()
        self._completed = completed

    @property
    def id(self) -> int:
        """Get the task ID."""
        return self._id

    @property
    def title(self) -> str:
        """Get the task title."""
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        """Set the task title after validation."""
        if not isinstance(value, str):
            raise ValueError("Title must be a string")

        if not value.strip():
            raise ValueError("Title cannot be empty or contain only whitespace")

        self._title = value.strip()

    @property
    def description(self) -> str:
        """Get the task description."""
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        """Set the task description."""
        if not isinstance(value, str):
            raise ValueError("Description must be a string")

        self._description = value.strip()

    @property
    def completed(self) -> bool:
        """Get the task completion status."""
        return self._completed

    @completed.setter
    def completed(self, value: bool) -> None:
        """Set the task completion status."""
        if not isinstance(value, bool):
            raise ValueError("Completed status must be a boolean")

        self._completed = value

    def to_dict(self) -> dict:
        """
        Convert the Task object to a dictionary representation.

        Returns:
            dict: Dictionary containing task attributes
        """
        return {
            "id": self._id,
            "title": self._title,
            "description": self._description,
            "completed": self._completed
        }

    def __repr__(self) -> str:
        """
        Return string representation of the Task object.

        Returns:
            str: String representation of the Task
        """
        status = "Completed" if self._completed else "Pending"
        return f"Task(id={self._id}, title='{self._title}', description='{self._description}', status={status})"

    def __eq__(self, other) -> bool:
        """
        Check equality between Task objects.

        Args:
            other: Another object to compare with

        Returns:
            bool: True if objects are equal, False otherwise
        """
        if not isinstance(other, Task):
            return False
        return (
            self._id == other._id and
            self._title == other._title and
            self._description == other._description and
            self._completed == other._completed
        )