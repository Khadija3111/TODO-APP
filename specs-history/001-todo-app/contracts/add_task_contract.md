# API Contract: Add Task

## Function Signature
```python
def add_task(title: str, description: str = "") -> dict:
    """
    Add a new task to the in-memory store.

    Args:
        title (str): The required title of the task
        description (str, optional): The optional description of the task

    Returns:
        dict: A dictionary containing:
            - 'success': bool indicating if the operation was successful
            - 'task_id': int the unique ID of the created task (if successful)
            - 'message': str describing the result
            - 'error': str describing the error (if unsuccessful)
    """
```

## Input Validation
- `title` must be a non-empty string after whitespace is trimmed
- `description` can be any string (including empty)
- If validation fails, return success=False with appropriate error message

## Success Response
```json
{
  "success": true,
  "task_id": 1,
  "message": "Task added successfully"
}
```

## Error Response
```json
{
  "success": false,
  "message": "Task title cannot be empty",
  "error": "validation_error"
}
```

## Business Rules
- Each task must have a unique ID that increments automatically
- New tasks are created with completed=False by default
- The title must be trimmed of leading/trailing whitespace before validation