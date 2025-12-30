# Data Model: Task Management System

## Task Entity

### Attributes
- **id**: `int` - Unique identifier for the task (auto-incrementing integer)
- **title**: `str` - Required title of the task (non-empty after trimming whitespace)
- **description**: `str` - Optional description of the task (can be empty)
- **completed**: `bool` - Status indicating if the task is completed (default: False)

### Validation Rules
- `id` must be a positive integer
- `title` must be a non-empty string after whitespace is trimmed
- `completed` must be a boolean value
- `description` can be any string (including empty)

### State Transitions
- A task starts with `completed = False`
- A task can transition from `completed = False` to `completed = True` (mark as complete)
- A task can transition from `completed = True` to `completed = False` (mark as incomplete)

## Task Store

### Structure
- **tasks**: `dict[int, Task]` - Dictionary mapping task IDs to Task objects
- **next_id**: `int` - The next available ID for new tasks (starts at 1)

### Operations
- **Create**: Add a new Task to the store with a unique ID
- **Read**: Retrieve a Task by its ID
- **Update**: Modify an existing Task's title or description
- **Delete**: Remove a Task by its ID
- **Toggle Completion**: Change a Task's completed status
- **List All**: Return all Tasks in the store