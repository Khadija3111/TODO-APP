"""
Task Name Resolution Logic
Helper functions to resolve ambiguous task references in user input
"""

import re
from typing import List, Optional, Dict, Any
from mcp.tools.task_operations import list_tasks_tool, ListTasksParams


async def resolve_task_by_reference(
    user_input: str,
    user_id: str,
    available_tasks: Optional[List[Dict[str, Any]]] = None
) -> Optional[Dict[str, Any]]:
    """
    Resolve a task reference from user input, which might be by ID, name, or description

    Args:
        user_input: The user's message that might contain a task reference
        user_id: The ID of the user whose tasks to search
        available_tasks: Pre-fetched list of tasks (optional, will fetch if not provided)

    Returns:
        The matching task dictionary or None if no clear match found
    """
    # Fetch tasks if not provided
    if available_tasks is None:
        list_params = ListTasksParams(user_id=user_id, status="all")
        tasks_result = await list_tasks_tool(list_params)
        available_tasks = tasks_result.get("tasks", [])

    # First, check if the input is just a number (like "4" from "task_id: '4'")
    # If so, treat it as a 1-based index (user says "task 4", meaning the 4th task)
    try:
        if user_input.isdigit():
            task_index = int(user_input) - 1  # Convert to 0-based index
            if 0 <= task_index < len(available_tasks):
                return available_tasks[task_index]
    except ValueError:
        pass

    # Look for task ID in the input (numbers) - try to match by position/index
    # Check if user provided a numeric position (like "task 1", "task 2")
    id_matches = re.findall(r'(?:task |^|no\.|\b)(\d+)(?:\b|$)', user_input.lower())
    if id_matches:
        try:
            # Convert to 0-based index
            task_index = int(id_matches[0]) - 1
            if 0 <= task_index < len(available_tasks):
                return available_tasks[task_index]
        except (ValueError, IndexError):
            pass

    # If not found by index, check if the input might be an actual UUID string
    # Check if the user_input itself looks like a UUID
    import uuid
    try:
        uuid.UUID(user_input)
        # If it's a valid UUID, look for exact match
        for task in available_tasks:
            if task.get('id', '') == user_input:
                return task
    except ValueError:
        # Not a UUID, continue with name matching
        pass

    # Look for exact name matches first
    for task in available_tasks:
        task_title = task.get('title', '').lower()
        if task_title == user_input.lower().strip():
            return task

    # Look for partial name matches
    potential_matches = []
    user_lower = user_input.lower()

    for task in available_tasks:
        task_title = task.get('title', '').lower()
        task_desc = task.get('description', '').lower() if task.get('description') else ""

        # Calculate similarity score
        score = 0
        if task_title in user_lower or user_lower in task_title:
            score += 100  # Exact substring match
        elif task_desc and (task_desc in user_lower or user_lower in task_desc):
            score += 50   # Description match

        # Word overlap scoring
        user_words = set(user_lower.split())
        task_words = set(task_title.split())
        overlap = len(user_words.intersection(task_words))
        if overlap > 0:
            score += overlap * 10

        if score > 0:
            potential_matches.append((task, score))

    # Sort by score and return the best match if it's significantly better than others
    if potential_matches:
        potential_matches.sort(key=lambda x: x[1], reverse=True)

        # If we have a clear winner (significantly higher score than second best)
        if len(potential_matches) == 1 or \
           (len(potential_matches) > 1 and
            potential_matches[0][1] > potential_matches[1][1] * 1.5):
            return potential_matches[0][0]

    return None


async def find_potential_task_matches(
    user_input: str,
    user_id: str
) -> List[Dict[str, Any]]:
    """
    Find all potential task matches for ambiguous references

    Args:
        user_input: The user's message that might contain a task reference
        user_id: The ID of the user whose tasks to search

    Returns:
        List of matching task dictionaries
    """
    # Fetch all tasks for the user
    list_params = ListTasksParams(user_id=user_id, status="all")
    tasks_result = await list_tasks_tool(list_params)
    available_tasks = tasks_result.get("tasks", [])

    # First check if the input is a simple number (like "2" from "task 2")
    # If so, return that specific indexed task
    id_matches = re.findall(r'^(\d+)$', user_input.strip())
    if id_matches:
        try:
            # Convert to 0-based index
            task_index = int(id_matches[0]) - 1
            if 0 <= task_index < len(available_tasks):
                return [available_tasks[task_index]]
        except (ValueError, IndexError):
            pass

    potential_matches = []
    user_lower = user_input.lower()

    for task in available_tasks:
        task_title = task.get('title', '').lower()
        task_desc = task.get('description', '').lower() if task.get('description') else ""

        # Calculate similarity score
        score = 0
        if task_title in user_lower or user_lower in task_title:
            score += 100  # Exact substring match
        elif task_desc and (task_desc in user_lower or user_lower in task_desc):
            score += 50   # Description match

        # Word overlap scoring
        user_words = set(user_lower.split())
        task_words = set(task_title.split())
        overlap = len(user_words.intersection(task_words))
        if overlap > 0:
            score += overlap * 10

        if score > 0:
            task_with_score = task.copy()
            task_with_score['_match_score'] = score
            potential_matches.append(task_with_score)

    # Sort by score descending
    potential_matches.sort(key=lambda x: x.get('_match_score', 0), reverse=True)
    # Remove the match score before returning
    for task in potential_matches:
        if '_match_score' in task:
            del task['_match_score']

    return potential_matches


def needs_clarification(user_input: str, potential_matches: List[Dict[str, Any]]) -> bool:
    """
    Determine if the user needs to clarify which task they mean

    Args:
        user_input: The user's original input
        potential_matches: List of potential task matches

    Returns:
        True if clarification is needed, False otherwise
    """
    # If there are no matches, no clarification needed (will be handled differently)
    if not potential_matches:
        return False

    # If there's only one match, probably no clarification needed
    if len(potential_matches) == 1:
        return False

    # Check if the user's input specifically indicates they want all matched tasks
    user_lower = user_input.lower()
    if any(word in user_lower for word in ['all', 'every', 'each']):
        return False  # User might want to act on all matches

    # If there are multiple matches of similar quality, clarification is needed
    return len(potential_matches) > 1