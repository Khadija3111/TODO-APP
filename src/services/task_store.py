"""
Task Store Service

This module provides the database storage and management for tasks using SQLModel and Neon PostgreSQL.
"""

from typing import List, Optional
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.models.task import Task, PriorityEnum
from sqlmodel import Session, select
from backend.utils.database import engine
from datetime import datetime


class TaskStore:
    """
    Database-based task storage and management service using SQLModel and Neon PostgreSQL.
    """

    def __init__(self):
        """
        Initialize the TaskStore by ensuring the database tables exist.
        """
        from backend.utils.database import create_db_and_tables
        create_db_and_tables()

    def add_task(self, title: str, description: str = "", priority: Optional[str] = None, tags: Optional[List[str]] = None) -> str:
        """
        Add a new task to the database with a unique ID.

        Args:
            title (str): The title of the task (required)
            description (str): The description of the task (optional)
            priority (str, optional): Priority level ('high', 'medium', 'low')
            tags (List[str], optional): List of tags for the task

        Returns:
            str: The ID of the newly created task

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

        # Convert priority to enum if provided
        priority_enum = None
        if priority:
            try:
                priority_enum = PriorityEnum(priority.lower())
            except ValueError:
                raise ValueError("Priority must be 'high', 'medium', or 'low'")

        with Session(engine) as session:
            # Create a new task
            task = Task(
                title=title.strip(),
                description=description.strip(),
                completed=False,
                priority=priority_enum,
            )

            # Set tags if provided
            if tags:
                task.set_tags(tags)

            # Add the task to the database
            session.add(task)
            session.commit()
            session.refresh(task)

            return task.id

    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Retrieve a task by its ID from the database.

        Args:
            task_id (str): The ID of the task to retrieve

        Returns:
            Task: The task with the specified ID, or None if not found
        """
        if not isinstance(task_id, str) or not task_id:
            raise ValueError("Task ID must be a non-empty string")

        with Session(engine) as session:
            statement = select(Task).where(Task.id == task_id)
            task = session.exec(statement).first()
            return task

    def update_task(self, task_id: str, title: Optional[str] = None, description: Optional[str] = None,
                    priority: Optional[str] = None, tags: Optional[List[str]] = None) -> bool:
        """
        Update an existing task's title, description, priority, or tags in the database.

        Args:
            task_id (str): The ID of the task to update
            title (str, optional): The new title for the task
            description (str, optional): The new description for the task
            priority (str, optional): The new priority for the task
            tags (List[str], optional): The new tags for the task

        Returns:
            bool: True if the task was updated successfully, False otherwise
        """
        if not isinstance(task_id, str) or not task_id:
            raise ValueError("Task ID must be a non-empty string")

        with Session(engine) as session:
            statement = select(Task).where(Task.id == task_id)
            result = session.exec(statement)
            task = result.first()

            if task is None:
                return False

            if title is not None:
                if not isinstance(title, str):
                    raise ValueError("Title must be a string")
                if not title.strip():
                    raise ValueError("Title cannot be empty or contain only whitespace")
                task.title = title.strip()

            if description is not None:
                if not isinstance(description, str):
                    raise ValueError("Description must be a string")
                task.description = description.strip()

            if priority is not None:
                if not isinstance(priority, str):
                    raise ValueError("Priority must be a string")
                try:
                    task.priority = PriorityEnum(priority.lower())
                except ValueError:
                    raise ValueError("Priority must be 'high', 'medium', or 'low'")

            if tags is not None:
                task.set_tags(tags)

            # Update the timestamp
            task.updated_at = datetime.now()

            session.add(task)
            session.commit()
            session.refresh(task)

            return True

    def delete_task(self, task_id: str) -> bool:
        """
        Remove a task by its ID from the database.

        Args:
            task_id (str): The ID of the task to delete

        Returns:
            bool: True if the task was deleted successfully, False otherwise
        """
        if not isinstance(task_id, str) or not task_id:
            raise ValueError("Task ID must be a non-empty string")

        with Session(engine) as session:
            statement = select(Task).where(Task.id == task_id)
            result = session.exec(statement)
            task = result.first()

            if task:
                session.delete(task)
                session.commit()
                return True
            return False

    def toggle_task_completion(self, task_id: str) -> bool:
        """
        Change a task's completed status in the database.

        Args:
            task_id (str): The ID of the task to toggle

        Returns:
            bool: True if the task status was toggled successfully, False otherwise
        """
        if not isinstance(task_id, str) or not task_id:
            raise ValueError("Task ID must be a non-empty string")

        with Session(engine) as session:
            statement = select(Task).where(Task.id == task_id)
            result = session.exec(statement)
            task = result.first()

            if task is None:
                return False

            task.completed = not task.completed
            task.updated_at = datetime.now()

            session.add(task)
            session.commit()
            session.refresh(task)

            return True

    def list_all_tasks(self) -> List[Task]:
        """
        Return all tasks from the database.

        Returns:
            List[Task]: A list of all tasks in the database
        """
        with Session(engine) as session:
            statement = select(Task)
            tasks = session.exec(statement).all()
            return tasks

    def get_all_tasks(self) -> List[Task]:
        """
        Return all tasks from the database (alias for list_all_tasks).

        Returns:
            List[Task]: A list of all tasks in the database
        """
        return self.list_all_tasks()

    def search_tasks(self, keyword: str) -> List[Task]:
        """
        Search tasks by keyword in title and description in the database.

        Args:
            keyword (str): The keyword to search for

        Returns:
            List[Task]: A list of tasks matching the search criteria
        """
        if not isinstance(keyword, str):
            raise ValueError("Keyword must be a string")

        with Session(engine) as session:
            statement = select(Task).where(
                (Task.title.contains(keyword)) | (Task.description.contains(keyword))
            )
            tasks = session.exec(statement).all()
            return tasks

    def filter_tasks(self, status: Optional[str] = None, priority: Optional[str] = None,
                     tags: Optional[List[str]] = None) -> List[Task]:
        """
        Filter tasks by status, priority, and/or tags in the database.

        Args:
            status (str, optional): Status to filter by ('all', 'pending', 'completed')
            priority (str, optional): Priority to filter by ('high', 'medium', 'low', 'any')
            tags (List[str], optional): Tags to filter by

        Returns:
            List[Task]: A list of tasks matching the filter criteria
        """
        with Session(engine) as session:
            statement = select(Task)

            # Filter by status
            if status and status.lower() != 'all':
                if status.lower() == 'pending':
                    statement = statement.where(Task.completed == False)
                elif status.lower() == 'completed':
                    statement = statement.where(Task.completed == True)

            # Filter by priority
            if priority and priority.lower() != 'any':
                try:
                    priority_enum = PriorityEnum(priority.lower())
                    statement = statement.where(Task.priority == priority_enum)
                except ValueError:
                    raise ValueError("Priority must be 'high', 'medium', 'low', or 'any'")

            tasks = session.exec(statement).all()

            # Filter by tags (needs to be done after DB query since tags are stored as JSON)
            if tags:
                filtered_tasks = []
                for task in tasks:
                    task_tags = set(task.tags_list)
                    filter_tags = set(tags)
                    if filter_tags.issubset(task_tags):
                        filtered_tasks.append(task)
                return filtered_tasks

            return tasks

    def sort_tasks(self, sort_field: str = 'created', sort_order: str = 'asc') -> List[Task]:
        """
        Sort tasks by the specified field and order in the database.

        Args:
            sort_field (str): Field to sort by ('created', 'priority', 'alpha', 'due')
            sort_order (str): Sort order ('asc' for ascending, 'desc' for descending)

        Returns:
            List[Task]: A sorted list of tasks
        """
        with Session(engine) as session:
            statement = select(Task)

            # Apply sorting based on field and order
            if sort_field == 'alpha':
                if sort_order == 'asc':
                    statement = statement.order_by(Task.title.asc())
                else:
                    statement = statement.order_by(Task.title.desc())
            elif sort_field == 'priority':
                if sort_order == 'asc':
                    statement = statement.order_by(Task.priority.asc())
                else:
                    statement = statement.order_by(Task.priority.desc())
            elif sort_field == 'created':
                if sort_order == 'asc':
                    statement = statement.order_by(Task.created_at.asc())
                else:
                    statement = statement.order_by(Task.created_at.desc())
            # Note: 'due' field not implemented in current model

            tasks = session.exec(statement).all()
            return tasks

    def get_next_id(self) -> str:
        """
        Get a new task ID (using UUID format).

        Returns:
            str: A new task ID in UUID format
        """
        import uuid
        return str(uuid.uuid4())

    def clear_all_tasks(self) -> None:
        """
        Remove all tasks from the database.
        """
        with Session(engine) as session:
            statement = select(Task)
            tasks = session.exec(statement).all()
            for task in tasks:
                session.delete(task)
            session.commit()