"""
MCP Server for Todo AI Chatbot
Exposes todo tools for the AI agent to interact with tasks
"""

import asyncio
from mcp.server import Server
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

# Import the database models and services
from sqlmodel import Session
from ..models.task import Task
from ..utils.database import get_session
from ..services.task_service import TaskService


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


class MCPServer:
    def __init__(self):
        self.server = Server("todo-mcp-server")
        self._register_tools()

    def _register_tools(self):
        """Register all todo tools with the MCP server"""

        @self.server.tool(
            "add_task",
            description="Add a new task for the user",
            input_schema=AddTaskParams.model_json_schema()
        )
        async def add_task(context, params: AddTaskParams) -> Dict[str, Any]:
            """
            Add a new task for the user
            """
            try:
                # Get database session
                with next(get_session()) as session:
                    task_service = TaskService(session)

                    # Create the task
                    task = await task_service.create_task(
                        user_id=params.user_id,
                        title=params.title,
                        description=params.description
                    )

                    return {
                        "success": True,
                        "task_id": task.id,
                        "title": task.title,
                        "completed": task.completed,
                        "message": f"Task '{task.title}' (ID: {task.id}) has been added successfully."
                    }
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Failed to add task: {str(e)}",
                    "message": f"Error: Could not add task '{params.title}'. {str(e)}"
                }

        @self.server.tool(
            "list_tasks",
            description="List tasks for the user with optional status filter",
            input_schema=ListTasksParams.model_json_schema()
        )
        async def list_tasks(context, params: ListTasksParams) -> Dict[str, Any]:
            """
            List tasks for the user with optional status filter
            """
            try:
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
                            "id": task.id,
                            "title": task.title,
                            "description": task.description,
                            "completed": task.completed
                        })

                    return {
                        "success": True,
                        "tasks": task_list,
                        "count": len(task_list),
                        "status_filter": params.status,
                        "message": f"Found {len(task_list)} {'completed' if params.status == 'completed' else 'pending' if params.status == 'pending' else 'total'} tasks for user {params.user_id}."
                    }
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Failed to list tasks: {str(e)}",
                    "message": f"Error: Could not retrieve tasks for user {params.user_id}. {str(e)}"
                }

        @self.server.tool(
            "complete_task",
            description="Mark a task as completed",
            input_schema=CompleteTaskParams.model_json_schema()
        )
        async def complete_task(context, params: CompleteTaskParams) -> Dict[str, Any]:
            """
            Mark a task as completed
            """
            try:
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
                        return {
                            "success": True,
                            "task_id": updated_task.id,
                            "title": updated_task.title,
                            "completed": updated_task.completed,
                            "message": f"Task '{updated_task.title}' (ID: {updated_task.id}) has been marked as completed."
                        }
                    else:
                        return {
                            "success": False,
                            "error": "Task not found",
                            "message": f"Error: Could not find task with ID {params.task_id} for user {params.user_id}."
                        }
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Failed to complete task: {str(e)}",
                    "message": f"Error: Could not complete task {params.task_id} for user {params.user_id}. {str(e)}"
                }

        @self.server.tool(
            "delete_task",
            description="Delete a task",
            input_schema=DeleteTaskParams.model_json_schema()
        )
        async def delete_task(context, params: DeleteTaskParams) -> Dict[str, Any]:
            """
            Delete a task
            """
            try:
                # Get database session
                with next(get_session()) as session:
                    task_service = TaskService(session)

                    # Delete the task
                    success = await task_service.delete_task(
                        user_id=params.user_id,
                        task_id=params.task_id
                    )

                    if success:
                        return {
                            "success": True,
                            "task_id": params.task_id,
                            "message": f"Task with ID {params.task_id} has been deleted successfully."
                        }
                    else:
                        return {
                            "success": False,
                            "error": "Task not found",
                            "message": f"Error: Could not find task with ID {params.task_id} for user {params.user_id}."
                        }
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Failed to delete task: {str(e)}",
                    "message": f"Error: Could not delete task {params.task_id} for user {params.user_id}. {str(e)}"
                }

        @self.server.tool(
            "update_task",
            description="Update a task's title or description",
            input_schema=UpdateTaskParams.model_json_schema()
        )
        async def update_task(context, params: UpdateTaskParams) -> Dict[str, Any]:
            """
            Update a task's title or description
            """
            try:
                # Get database session
                with next(get_session()) as session:
                    task_service = TaskService(session)

                    # Prepare update data
                    update_data = {}
                    if params.title is not None:
                        update_data['title'] = params.title
                    if params.description is not None:
                        update_data['description'] = params.description

                    # Update the task
                    updated_task = await task_service.update_task_details(
                        user_id=params.user_id,
                        task_id=params.task_id,
                        title=params.title,
                        description=params.description,
                        priority=params.priority
                    )

                    if updated_task:
                        return {
                            "success": True,
                            "task_id": updated_task.id,
                            "title": updated_task.title,
                            "description": updated_task.description,
                            "completed": updated_task.completed,
                            "message": f"Task (ID: {updated_task.id}) has been updated successfully."
                        }
                    else:
                        return {
                            "success": False,
                            "error": "Task not found",
                            "message": f"Error: Could not find task with ID {params.task_id} for user {params.user_id}."
                        }
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Failed to update task: {str(e)}",
                    "message": f"Error: Could not update task {params.task_id} for user {params.user_id}. {str(e)}"
                }

    async def start(self, host: str = "localhost", port: int = 3000):
        """Start the MCP server"""
        await self.server.run_tcp(host, port)


# Global server instance
mcp_server = MCPServer()


async def run_mcp_server():
    """Function to run the MCP server"""
    await mcp_server.start()


if __name__ == "__main__":
    asyncio.run(run_mcp_server())