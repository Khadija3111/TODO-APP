from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session, select
from typing import List

from models.task import Task, TaskCreate, TaskRead, TaskUpdate
from models.user import User
from utils.auth import get_current_user
from utils.database import get_session

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=List[TaskRead])
def get_tasks(
    completed: bool = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all tasks for the current user, optionally filtered by completion status."""
    statement = select(Task).where(Task.user_id == current_user.id)

    if completed is not None:
        statement = statement.where(Task.completed == completed)

    tasks = session.exec(statement).all()
    return tasks

@router.post("/", response_model=TaskRead)
def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new task for the current user."""
    db_task = Task(
        **task.dict(),
        user_id=current_user.id
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a specific task by ID."""
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task"
        )
    return task

@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: str,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a specific task by ID."""
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    # Update the task with the provided fields
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.put("/{task_id}/complete", response_model=TaskRead)
def toggle_task_completion(
    task_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Toggle the completion status of a specific task by ID."""
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    # Toggle the completion status
    task.completed = not task.completed
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.delete("/{task_id}")
def delete_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a specific task by ID."""
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )

    session.delete(task)
    session.commit()
    return {"message": "Task deleted successfully"}