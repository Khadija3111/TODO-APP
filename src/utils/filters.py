"""
Filter utility functions for the Todo application.

This module provides functions to filter tasks based on various criteria.
"""
from typing import List, Optional
from models.task import Task


def filter_by_status(tasks: List[Task], status: Optional[str]) -> List[Task]:
    """
    Filter tasks by completion status.

    Args:
        tasks: List of tasks to filter
        status: Status to filter by ('all', 'pending', 'completed', or None for no filter)

    Returns:
        List of tasks matching the status
    """
    if not status or status.lower() == 'all':
        return tasks

    status_lower = status.lower()
    if status_lower == 'pending':
        return [task for task in tasks if not task.completed]
    elif status_lower == 'completed':
        return [task for task in tasks if task.completed]
    else:
        # If invalid status, return all tasks
        return tasks


def filter_by_priority(tasks: List[Task], priority: Optional[str]) -> List[Task]:
    """
    Filter tasks by priority level.

    Args:
        tasks: List of tasks to filter
        priority: Priority to filter by ('high', 'medium', 'low', 'any', or None for no filter)

    Returns:
        List of tasks matching the priority
    """
    if not priority or priority.lower() == 'any':
        return tasks

    priority_lower = priority.lower()
    if tasks and hasattr(tasks[0], 'priority'):
        return [task for task in tasks if
                hasattr(task, 'priority') and
                task.priority and
                task.priority.lower() == priority_lower]
    else:
        # If tasks don't have priority attribute, return all
        return tasks


def filter_by_tags(tasks: List[Task], tags: Optional[List[str]]) -> List[Task]:
    """
    Filter tasks by tags.

    Args:
        tasks: List of tasks to filter
        tags: List of tags to filter by

    Returns:
        List of tasks that contain any of the specified tags
    """
    if not tags:
        return tasks

    # Convert all tags to lowercase for case-insensitive matching
    tag_set = {tag.lower().strip() for tag in tags if tag.strip()}

    if not tag_set:
        return tasks

    filtered_tasks = []
    for task in tasks:
        if hasattr(task, 'tags') and task.tags:
            # Check if any of the task's tags match the filter tags
            task_tags_lower = {tag.lower().strip() for tag in task.tags}
            if tag_set.intersection(task_tags_lower):
                filtered_tasks.append(task)

    return filtered_tasks


def apply_filters(tasks: List[Task],
                 status: Optional[str] = None,
                 priority: Optional[str] = None,
                 tags: Optional[List[str]] = None) -> List[Task]:
    """
    Apply multiple filters to a list of tasks.

    Args:
        tasks: List of tasks to filter
        status: Status filter
        priority: Priority filter
        tags: Tags filter

    Returns:
        List of tasks that match all specified filters
    """
    result = tasks

    if status is not None:
        result = filter_by_status(result, status)

    if priority is not None:
        result = filter_by_priority(result, priority)

    if tags is not None:
        result = filter_by_tags(result, tags)

    return result