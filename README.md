# Todo Console Application

A simple, in-memory todo list application built with Python 3.13+.

## Setup

1. Ensure Python 3.13+ is installed on your system
2. Clone the repository
3. Navigate to the project directory
4. Run the application with Python

## Running the Application

```bash
cd src
python main.py
```

## Features

- Add tasks with title and optional description
- View all tasks with their completion status
- Update task title and description
- Delete tasks
- Mark tasks as complete/incomplete

## Example Usage

### Add Task
```
Welcome to the Todo Application!
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Toggle Task Completion
6. Exit

Enter your choice: 1
Enter task title: Buy groceries
Enter task description (optional): Need to buy milk and bread
Task added successfully with ID: 1
```

### View Tasks
```
Enter your choice: 2

--- Tasks ---
ID: 1 | Title: Buy groceries | Description: Need to buy milk and bread | Status: Pending
ID: 2 | Title: Walk the dog | Description:  | Status: Completed
```

### Update Task
```
Enter your choice: 3

--- Update Task ---
Enter task ID to update: 1
Current task: Buy groceries
Enter new title (current: 'Buy groceries', press Enter to keep current): Buy weekly groceries
Enter new description (current: 'Need to buy milk and bread', press Enter to keep current): Need to buy milk, bread, eggs, and fruit
Task 1 updated successfully.
```

### Delete Task
```
Enter your choice: 4

--- Delete Task ---
Enter task ID to delete: 2
Task 2 deleted successfully.
```

### Toggle Task Completion
```
Enter your choice: 5

--- Toggle Task Completion ---
Enter task ID to toggle completion: 1
Task 1 marked as completed.
```

## Development

To run the application in development mode:
```bash
cd src
python main.py
```

## Architecture

The application follows a clean architecture with:
- Models in `src/models/`
- Services in `src/services/`
- CLI interface in `src/cli/`
- Main application entry point in `main.py`