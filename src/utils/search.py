"""
Search utility functions for the Todo application.

This module provides functions to search tasks by keywords in title and description.
"""
from typing import List
from models.task import Task


def search_tasks(tasks: List[Task], keyword: str) -> List[Task]:
    """
    Search tasks by keyword in title, description, and tags.

    Args:
        tasks: List of tasks to search through
        keyword: Keyword to search for (case-insensitive, partial match)

    Returns:
        List of tasks that contain the keyword in title, description, or tags
    """
    if not keyword:
        return []

    keyword_lower = keyword.lower().strip()
    if not keyword_lower:
        return []

    matching_tasks = []
    for task in tasks:
        # Check if keyword is in title (case-insensitive)
        title_match = keyword_lower in task.title.lower()

        # Check if keyword is in description (case-insensitive)
        description_match = keyword_lower in task.description.lower()

        # Check if keyword is in any of the tags (case-insensitive)
        tag_match = any(keyword_lower in tag.lower() for tag in task.tags)

        # Add task to results if keyword is found in title, description, or tags
        if title_match or description_match or tag_match:
            matching_tasks.append(task)

    return matching_tasks