"""
Rendering utilities for the Todo application.

This module provides functions for formatting task output with ANSI colors.
"""

from models.task import Task
from typing import List


def format_task_output(task: Task, use_color: bool = True) -> str:
    """
    Format a single task for display with optional ANSI colors.

    Args:
        task: The task to format
        use_color: Whether to use ANSI colors in the output

    Returns:
        Formatted string representation of the task
    """
    if use_color:
        # ANSI color codes
        RED = '\033[31m'      # Red for overdue/completed tasks
        GREEN = '\033[32m'    # Green for completed tasks
        YELLOW = '\033[33m'   # Yellow for high priority
        BLUE = '\033[34m'     # Blue for medium priority
        MAGENTA = '\033[35m'  # Magenta for low priority
        CYAN = '\033[36m'     # Cyan for tags
        RESET = '\033[0m'     # Reset to default color

        status = "Completed" if task.completed else "Pending"
        status_color = GREEN if task.completed else RED
        status_str = f"{status_color}{status}{RESET}"

        priority_str = ""
        if task.priority:
            priority_colors = {
                'high': YELLOW,
                'medium': BLUE,
                'low': MAGENTA
            }
            color = priority_colors.get(task.priority.lower(), RESET)
            priority_str = f", Priority: {color}{task.priority}{RESET}"

        tags_str = ""
        if task.tags:
            tags_display = f"{CYAN}[{', '.join(task.tags)}]{RESET}"
            tags_str = f", Tags: {tags_display}"

        return f"ID: {task.id} | Title: {task.title} | Description: {task.description} | Status: {status_str}{priority_str}{tags_str}"
    else:
        # Plain text without colors
        status = "Completed" if task.completed else "Pending"
        priority_str = f", Priority: {task.priority}" if task.priority else ""
        tags_str = f", Tags: [{', '.join(task.tags)}]" if task.tags else ""
        return f"ID: {task.id} | Title: {task.title} | Description: {task.description} | Status: {status} | Priority: {task.priority}{tags_str}"


def format_tasks_list(tasks: List[Task], use_color: bool = True) -> str:
    """
    Format a list of tasks for display.

    Args:
        tasks: List of tasks to format
        use_color: Whether to use ANSI colors in the output

    Returns:
        Formatted string representation of the task list
    """
    if not tasks:
        return "No tasks found."

    output_lines = []
    for task in tasks:
        output_lines.append(format_task_output(task, use_color))

    return "\n".join(output_lines)


def print_colored_message(message: str, color: str = None) -> None:
    """
    Print a message with optional color.

    Args:
        message: The message to print
        color: The color to use (if None, prints without color)
    """
    if color:
        RESET = '\033[0m'
        print(f"{color}{message}{RESET}")
    else:
        print(message)