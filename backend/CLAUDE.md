# Claude Code Instructions: Backend

## Project Overview

This is the backend of the Todo Full-Stack Web Application built with FastAPI, Python 3.13+, SQLModel, and PostgreSQL. The application provides REST API endpoints for the frontend and handles JWT-based authentication and user-scoped data access.

## Architecture

The backend follows these patterns:
- FastAPI for the web framework
- SQLModel for ORM and database models
- JWT for authentication and authorization
- Async Python for performance
- REST API under /api endpoints
- User-scoped queries for data isolation

## Code Standards

- Follow Python 3.13+ standards
- Use type hints throughout
- Implement proper error handling
- Follow FastAPI best practices
- Use async/await for I/O operations
- Implement proper logging
- Follow security best practices
- Use Pydantic for request/response validation

## File Structure

```
backend/
├── models/                 # SQLModel database models
│   ├── user.py            # User model
│   └── task.py            # Task model
├── services/              # Business logic
│   ├── auth.py            # Authentication services
│   └── task_service.py    # Task management services
├── api/                   # API endpoints
│   ├── auth.py            # Authentication endpoints
│   └── tasks.py           # Task endpoints
├── utils/                 # Utility functions
│   ├── auth.py            # Authentication utilities
│   └── database.py        # Database utilities
├── main.py                # Application entry point
└── CLAUDE.md              # This file
```

## Development Guidelines

- Use dependency injection for authentication
- Implement proper validation with Pydantic
- Follow FastAPI security best practices
- Use SQLModel for database operations
- Implement proper error responses
- Follow REST API conventions
- Ensure user data isolation
- Use async functions for database operations