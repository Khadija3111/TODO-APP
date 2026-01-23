"""
MCP Tools for Todo Operations
Contains the individual task operation tools for the MCP server
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import json
import uuid
import logging

# Import the database models and services
from sqlmodel import Session, select
from models.task import Task
from utils.database import get_session
from services.task_service import TaskService

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AddTaskParams(BaseModel):
    user_id: str = Field(..., description="User ID")
    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(None, description="Task description")


class ListTasksParams(BaseModel):
    user_id: str = Field(..., description="User ID")
    status: Optional[str] = Field("all", description="Filter status: all, pending, completed")


class CompleteTaskParams(BaseModel):
    user_id: str = Field(..., description="User ID")
    task_id: str = Field(..., description="Task ID to complete")


class DeleteTaskParams(BaseModel):
    user_id: str = Field(..., description="User ID")
    task_id: str = Field(..., description="Task ID to delete")


class UpdateTaskParams(BaseModel):
    user_id: str = Field(..., description="User ID")
    task_id: str = Field(..., description="Task ID to update")
    title: Optional[str] = Field(None, description="New task title")
    description: Optional[str] = Field(None, description="New task description")
    priority: Optional[str] = Field(None, description="New task priority (high, medium, low)")


async def add_task_tool(params: AddTaskParams) -> Dict[str, Any]:
    """
    Add a new task for the user
    """
    try:
        # Validate user_id format
        try:
            uuid.UUID(params.user_id)
        except ValueError:
            return {
                "success": False,
                "error": "Invalid user ID format",
                "message": f"Error: Invalid user ID format '{params.user_id}'. User ID must be a valid UUID."
            }

        # Get database session
        with next(get_session()) as session:
            task_service = TaskService(session)

            # Create the task
            task = await task_service.create_task(
                user_id=params.user_id,
                title=params.title,
                description=params.description
            )

            logger.info(f"Task added successfully: {task.id} for user {params.user_id}")

            return {
                "success": True,
                "task_id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "priority": getattr(task, 'priority', 'medium'),  # Default to medium if not set
                "category": getattr(task, 'category', ''),
                "message": f"Task '{task.title}' (ID: {task.id}) has been added successfully."
            }
    except Exception as e:
        logger.error(f"Failed to add task: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to add task: {str(e)}",
            "message": f"Error: Could not add task '{params.title}'. {str(e)}"
        }


async def list_tasks_tool(params: ListTasksParams) -> Dict[str, Any]:
    """
    List tasks for the user with optional status filter
    """
    try:
        # Validate user_id format
        try:
            uuid.UUID(params.user_id)
        except ValueError:
            return {
                "success": False,
                "error": "Invalid user ID format",
                "message": f"Error: Invalid user ID format '{params.user_id}'. User ID must be a valid UUID."
            }

        # Get database session
        with next(get_session()) as session:
            task_service = TaskService(session)

            # Get tasks based on status filter
            if params.status == "pending":
                tasks = await task_service.get_pending_tasks(params.user_id)
            elif params.status == "completed":
                tasks = await task_service.get_completed_tasks(params.user_id)
            else:  # all
                tasks = await task_service.get_all_tasks(params.user_id)

            task_list = []
            for task in tasks:
                task_list.append({
                    "id": str(task.id),  # Ensure ID is string
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "priority": getattr(task, 'priority', 'medium'),
                    "category": getattr(task, 'category', ''),
                    "created_at": task.created_at.isoformat() if hasattr(task, 'created_at') and task.created_at else None,
                    "updated_at": task.updated_at.isoformat() if hasattr(task, 'updated_at') and task.updated_at else None
                })

            logger.info(f"Listed {len(task_list)} tasks for user {params.user_id}")

            return {
                "success": True,
                "tasks": task_list,
                "count": len(task_list),
                "status_filter": params.status,
                "message": f"Found {len(task_list)} {'completed' if params.status == 'completed' else 'pending' if params.status == 'pending' else 'total'} tasks for user {params.user_id}."
            }
    except Exception as e:
        logger.error(f"Failed to list tasks: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to list tasks: {str(e)}",
            "message": f"Error: Could not retrieve tasks for user {params.user_id}. {str(e)}"
        }


async def complete_task_tool(params: CompleteTaskParams) -> Dict[str, Any]:
    """
    Mark a task as completed
    """
    try:
        # Validate user_id format
        try:
            uuid.UUID(params.user_id)
        except ValueError:
            return {
                "success": False,
                "error": "Invalid user ID format",
                "message": f"Error: Invalid user ID format '{params.user_id}'. User ID must be a valid UUID."
            }

        # Get database session
        with next(get_session()) as session:
            task_service = TaskService(session)

            # Update the task
            updated_task = await task_service.update_task_status(
                user_id=params.user_id,
                task_id=params.task_id,
                completed=True
            )

            if updated_task:
                logger.info(f"Task completed: {updated_task.id} for user {params.user_id}")

                return {
                    "success": True,
                    "task_id": str(updated_task.id),
                    "title": updated_task.title,
                    "completed": updated_task.completed,
                    "priority": getattr(updated_task, 'priority', 'medium'),
                    "category": getattr(updated_task, 'category', ''),
                    "message": f"Task '{updated_task.title}' (ID: {updated_task.id}) has been marked as completed."
                }
            else:
                logger.warning(f"Task not found: {params.task_id} for user {params.user_id}")

                return {
                    "success": False,
                    "error": "Task not found",
                    "message": f"Error: Could not find task with ID {params.task_id} for user {params.user_id}."
                }
    except Exception as e:
        logger.error(f"Failed to complete task: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to complete task: {str(e)}",
            "message": f"Error: Could not complete task {params.task_id} for user {params.user_id}. {str(e)}"
        }


async def delete_task_tool(params: DeleteTaskParams) -> Dict[str, Any]:
    """
    Delete a task
    """
    try:
        # Validate user_id format
        try:
            uuid.UUID(params.user_id)
        except ValueError:
            return {
                "success": False,
                "error": "Invalid user ID format",
                "message": f"Error: Invalid user ID format '{params.user_id}'. User ID must be a valid UUID."
            }

        # Get database session
        with next(get_session()) as session:
            task_service = TaskService(session)

            # Delete the task
            success = await task_service.delete_task(
                user_id=params.user_id,
                task_id=params.task_id
            )

            if success:
                logger.info(f"Task deleted: {params.task_id} for user {params.user_id}")

                return {
                    "success": True,
                    "task_id": params.task_id,
                    "message": f"Task with ID {params.task_id} has been deleted successfully."
                }
            else:
                logger.warning(f"Task not found for deletion: {params.task_id} for user {params.user_id}")

                return {
                    "success": False,
                    "error": "Task not found",
                    "message": f"Error: Could not find task with ID {params.task_id} for user {params.user_id}."
                }
    except Exception as e:
        logger.error(f"Failed to delete task: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to delete task: {str(e)}",
            "message": f"Error: Could not delete task {params.task_id} for user {params.user_id}. {str(e)}"
        }


async def update_task_tool(params: UpdateTaskParams) -> Dict[str, Any]:
    """
    Update a task's title or description
    """
    try:
        # Validate user_id format
        try:
            uuid.UUID(params.user_id)
        except ValueError:
            return {
                "success": False,
                "error": "Invalid user ID format",
                "message": f"Error: Invalid user ID format '{params.user_id}'. User ID must be a valid UUID."
            }

        # Get database session
        with next(get_session()) as session:
            task_service = TaskService(session)

            # Update the task
            updated_task = await task_service.update_task_details(
                user_id=params.user_id,
                task_id=params.task_id,
                title=params.title,
                description=params.description,
                priority=params.priority
            )

            if updated_task:
                logger.info(f"Task updated: {updated_task.id} for user {params.user_id}")

                return {
                    "success": True,
                    "task_id": str(updated_task.id),
                    "title": updated_task.title,
                    "description": updated_task.description,
                    "completed": updated_task.completed,
                    "priority": getattr(updated_task, 'priority', 'medium'),
                    "category": getattr(updated_task, 'category', ''),
                    "message": f"Task (ID: {updated_task.id}) has been updated successfully."
                }
            else:
                logger.warning(f"Task not found for update: {params.task_id} for user {params.user_id}")

                return {
                    "success": False,
                    "error": "Task not found",
                    "message": f"Error: Could not find task with ID {params.task_id} for user {params.user_id}."
                }
    except Exception as e:
        logger.error(f"Failed to update task: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to update task: {str(e)}",
            "message": f"Error: Could not update task {params.task_id} for user {params.user_id}. {str(e)}"
        }