# Quickstart: Todo Console Application

## Setup

1. Ensure Python 3.13+ is installed on your system
2. Clone the repository
3. Navigate to the project directory

## Running the Application

```bash
cd src
python main.py
```

## Using the Add Task Feature

1. Run the application
2. Select the "Add Task" option from the main menu
3. Enter the task title when prompted (required)
4. Optionally enter a task description when prompted
5. The application will confirm the task has been added with its unique ID

## Example Usage

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

## Development

To run the application in development mode:
```bash
cd src
python main.py
```

To run tests (if any exist):
```bash
python -m unittest discover tests/
```