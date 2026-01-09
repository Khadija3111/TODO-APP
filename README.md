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

### Basic Features
- Add tasks with title and optional description
- View all tasks with their completion status
- Update task title and description
- Delete tasks
- Mark tasks as complete/incomplete

### Intermediate Features
- **Priorities**: Assign priority levels (high/medium/low) to tasks
- **Tags**: Add one or more tags to tasks for better organization
- **Search**: Find tasks by keywords in title or description
- **Filter**: Filter tasks by status, priority, and tags
- **Sort**: Sort tasks by due date, priority, alphabetical, or creation date
- **Configuration**: Persistent sort preferences stored in config file
- **ANSI Colors**: Enhanced output with color coding for better readability

## Example Usage

### Add Task
```
Welcome to the Todo Application!
1. Add Task
2. View Tasks (with optional filtering and sorting)
3. Update Task
4. Delete Task
5. Toggle Task Completion
6. Search Tasks
7. Help
8. Exit

Enter your choice: 1
Enter task title: Buy groceries
Enter task description (optional): Need to buy milk and bread
Enter priority (high/medium/low, optional): high
Enter tags (comma-separated, optional): shopping,urgent
Task added successfully with ID: 1
Priority: high
Tags: shopping, urgent
```

### View Tasks with Filters and Sorting
```
Enter your choice: 2

--- Tasks ---
Filter options (press Enter to skip):
Filter by status (all/pending/completed): pending
Filter by priority (high/medium/low/any): high
Filter by tags (comma-separated): urgent
Sort options (press Enter to use default from config):
Sort by (created/priority/alpha/due): priority
Sort order (asc/desc): desc
Displaying 1 task(s), sorted by priority (desc):
ID: 1 | Title: Buy groceries | Description: Need to buy milk and bread | Status: Pending, Priority: high, Tags: [urgent, shopping]
```

### Search Tasks
```
Enter your choice: 6

--- Search Tasks ---
Enter search keyword: groceries
Found 1 task(s) matching 'groceries':
ID: 1 | Title: Buy groceries | Description: Need to buy milk and bread | Status: Pending, Priority: high, Tags: [urgent, shopping]
```

### Update Task
```
Enter your choice: 3

--- Update Task ---
Enter task ID to update: 1
Current task: Buy groceries
Enter new title (current: 'Buy groceries', press Enter to keep current): Buy weekly groceries
Enter new description (current: 'Need to buy milk and bread', press Enter to keep current): Need to buy milk, bread, eggs, and fruit
Enter new priority (high/medium/low, current: 'high', press Enter to keep current): medium
Enter new tags (comma-separated, current: 'urgent, shopping', press Enter to keep current): shopping,weekly
Task 1 updated successfully.
New priority: medium
New tags: shopping, weekly
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

### Running with No Color
To run the application without ANSI colors:
```bash
python main.py --no-color
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