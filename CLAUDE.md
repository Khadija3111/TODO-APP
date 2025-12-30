# Claude Code Instructions

This file contains instructions for Claude Code when working with this project.

## Project Overview

This is an in-memory Todo CLI application built with Python 3.13+. The application allows users to:
- Add tasks with title and optional description
- View all tasks with their completion status
- Update task title and description
- Delete tasks
- Mark tasks as complete/incomplete

## Architecture

The application follows a clean architecture with separation of concerns:
- **Models** (`src/models/`): Data models and validation
- **Services** (`src/services/`): Business logic and data storage
- **CLI** (`src/cli/`): User interface and input handling
- **Main** (`main.py`): Application entry point and orchestration

## Code Standards

- Follow Python 3.13+ standards
- Use clear, descriptive variable and function names
- Maintain single responsibility principle
- Include docstrings for all public functions
- Handle errors gracefully without crashing the application
- Use type hints where appropriate

## File Structure

```
src/
├── models/
│   └── task.py          # Task data model definition
├── services/
│   └── task_store.py    # In-memory task storage and management
├── cli/
│   └── cli_interface.py # Command-line interface and user interaction
└── main.py              # Application entry point
```

## Development Guidelines

- Always maintain in-memory storage only (no file/database persistence)
- Follow the existing code style and patterns
- Ensure all user inputs are validated
- Provide clear error messages to users
- Keep functions focused on a single responsibility