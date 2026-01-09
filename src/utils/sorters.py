"""
Sort utility functions for the Todo application.

This module provides functions to sort tasks by various criteria.
"""
from typing import List, Literal, Callable
from models.task import Task


def sort_tasks(tasks: List[Task],
              sort_field: Literal['created', 'priority', 'alpha', 'due'] = 'created',
              sort_order: Literal['asc', 'desc'] = 'asc') -> List[Task]:
    """
    Sort tasks by specified field and order.

    Args:
        tasks: List of tasks to sort
        sort_field: Field to sort by ('created', 'priority', 'alpha', 'due')
        sort_order: Sort order ('asc' for ascending, 'desc' for descending)

    Returns:
        List of tasks sorted according to the specified criteria
    """
    # Define sort key functions for each field
    sort_key_functions: dict[str, Callable[[Task], any]] = {
        'alpha': lambda task: task.title.lower(),
        'created': lambda task: task.id,  # Using ID as proxy for creation order
        'priority': lambda task: _get_priority_value(task),
        'due': lambda task: getattr(task, 'due_date', None) or ''  # Assuming due_date attribute
    }

    # Get the appropriate sort key function
    key_func = sort_key_functions.get(sort_field, sort_key_functions['created'])

    # Sort the tasks
    sorted_tasks = sorted(tasks, key=key_func, reverse=(sort_order == 'desc'))

    return sorted_tasks


def _get_priority_value(task: Task) -> int:
    """
    Convert priority string to numeric value for sorting.

    Args:
        task: Task object to get priority value for

    Returns:
        Numeric value for priority (high=3, medium=2, low=1, unknown=0)
    """
    if hasattr(task, 'priority') and task.priority:
        priority_map = {
            'high': 3,
            'medium': 2,
            'low': 1
        }
        return priority_map.get(task.priority.lower(), 0)
    return 0  # Default value for tasks without priority