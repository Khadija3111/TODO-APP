"""
Service layer for task management
Handles business logic for creating, reading, updating, and deleting tasks
"""

from typing import List, Optional
from datetime import datetime
from sqlmodel import Session, select

from models.task import Task, TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, session: Session):
        self.session = session

    async def create_task(
        self,
        user_id: str,
        title: str,
        description: Optional[str] = None
    ) -> Task:
        """
        Create a new task for a user
        """
        task = Task(
            user_id=user_id,
            title=title,
            description=description
        )
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    async def get_all_tasks(self, user_id: str) -> List[Task]:
        """
        Get all tasks for a user
        """
        statement = select(Task).where(Task.user_id == user_id)
        return self.session.exec(statement).all()

    async def get_pending_tasks(self, user_id: str) -> List[Task]:
        """
        Get all pending tasks for a user
        """
        statement = select(Task).where(
            Task.user_id == user_id,
            Task.completed == False
        )
        return self.session.exec(statement).all()

    async def get_completed_tasks(self, user_id: str) -> List[Task]:
        """
        Get all completed tasks for a user
        """
        statement = select(Task).where(
            Task.user_id == user_id,
            Task.completed == True
        )
        return self.session.exec(statement).all()

    async def get_task_by_id(self, user_id: str, task_id: str) -> Optional[Task]:
        """
        Get a specific task by ID for a user
        """
        statement = select(Task).where(
            Task.user_id == user_id,
            Task.id == task_id
        )
        return self.session.exec(statement).first()

    async def update_task_status(
        self,
        user_id: str,
        task_id: str,
        completed: bool
    ) -> Optional[Task]:
        """
        Update the completion status of a task
        """
        task = await self.get_task_by_id(user_id, task_id)
        if task:
            task.completed = completed
            task.updated_at = datetime.now()
            self.session.add(task)
            self.session.commit()
            self.session.refresh(task)
        return task

    async def update_task_details(
        self,
        user_id: str,
        task_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[str] = None
    ) -> Optional[Task]:
        """
        Update task details (title, description, priority)
        """
        task = await self.get_task_by_id(user_id, task_id)
        if task:
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            if priority is not None:
                # Validate priority value
                if priority in ['high', 'medium', 'low']:
                    task.priority = priority
                else:
                    # If priority is not valid, log a warning but continue with other updates
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.warning(f"Invalid priority value '{priority}' for task {task_id}. Valid values are: high, medium, low")
            task.updated_at = datetime.now()
            self.session.add(task)
            self.session.commit()
            self.session.refresh(task)
        return task

    async def delete_task(
        self,
        user_id: str,
        task_id: str
    ) -> bool:
        """
        Delete a task
        """
        task = await self.get_task_by_id(user_id, task_id)
        if task:
            self.session.delete(task)
            self.session.commit()
            return True
        return False

    async def get_task_count(self, user_id: str) -> int:
        """
        Get the total count of tasks for a user
        """
        statement = select(Task).where(Task.user_id == user_id)
        tasks = self.session.exec(statement).all()
        return len(tasks)

    async def get_task_stats(self, user_id: str) -> dict:
        """
        Get task statistics for a user
        """
        all_tasks = await self.get_all_tasks(user_id)
        total = len(all_tasks)
        completed = sum(1 for task in all_tasks if task.completed)
        pending = total - completed

        return {
            "total": total,
            "completed": completed,
            "pending": pending
        }