"""
Input Validation Functions

This module provides validation functions for task creation and other inputs.
"""


def validate_task_title(title: str) -> tuple[bool, str]:
    """
    Validate the task title.

    Args:
        title (str): The title to validate

    Returns:
        tuple[bool, str]: A tuple containing (is_valid, error_message)
    """
    if not isinstance(title, str):
        return False, "Title must be a string"

    if not title.strip():
        return False, "Title cannot be empty or contain only whitespace"

    return True, ""


def validate_task_description(description: str) -> tuple[bool, str]:
    """
    Validate the task description.

    Args:
        description (str): The description to validate

    Returns:
        tuple[bool, str]: A tuple containing (is_valid, error_message)
    """
    if not isinstance(description, str):
        return False, "Description must be a string"

    return True, ""


def validate_task_id(task_id: int) -> tuple[bool, str]:
    """
    Validate the task ID.

    Args:
        task_id (int): The task ID to validate

    Returns:
        tuple[bool, str]: A tuple containing (is_valid, error_message)
    """
    if not isinstance(task_id, int) or task_id <= 0:
        return False, "Task ID must be a positive integer"

    return True, ""