<!--
Sync Impact Report:
- Version change: 1.0.0 → 1.1.0
- Modified principles: Updated all principles to align with Phase I Todo Application
- Added sections: Phase I specific requirements and constraints
- Removed sections: Web framework, database, and cloud deployment requirements (out of scope for Phase I)
- Templates requiring updates:
  - .specify/templates/plan-template.md ✅ updated
  - .specify/templates/spec-template.md ✅ updated
  - .specify/templates/tasks-template.md ✅ updated
  - .specify/templates/commands/*.md ⚠ pending
- Follow-up TODOs: None
-->
# Phase I – In-Memory Todo Python Console Application Constitution

## Core Principles

### Spec-First Development
All implementation must originate from written specifications.

### Single Source of Truth
Specs define behavior; code must conform to specs, not vice versa.

### In-Memory Data Storage
All tasks must be stored in memory only using Python data structures. No external storage, databases, or file persistence mechanisms are allowed.

### Clean Console Interface
The application must provide a clear, text-based command-line interface with intuitive prompts and graceful error handling.

### Single Responsibility Principle
Functions should do one thing and do it well, with clear separation of concerns between data management, user interaction, and business logic.

### Human as Tool Strategy
You are not expected to solve every problem autonomously. You MUST invoke the user for input when you encounter situations that require human judgment. Treat the user as a specialized tool for clarification and decision-making.

## Key Standards and Constraints
- All features must be explicitly defined in `/specs-history` before implementation.
- Each feature must be implemented through a written specification stored chronologically in `/specs-history/`.
- No feature may be implemented without an approved spec.
- **Language**: Python 3.13+
- **Environment Management**: UV
- **Application Type**: Console/Command-Line Interface only
- **Data Storage**: In-memory Python data structures only (no files, databases, or external storage)
- **Data Persistence**: Not required across program restarts
- **No hardcoded secrets** in source code.
- User input must be validated gracefully without crashing the application.
- The program must clearly guide the user with prompts.

## Core Features (Phase I Only)
The application MUST implement exactly these five core features:

1. **Add Task**: Create a new task with a title and optional description
2. **View Tasks**: Display all tasks showing unique ID, title, description, and completion status
3. **Update Task**: Modify the title and/or description of an existing task using its ID
4. **Delete Task**: Remove a task permanently using its ID
5. **Mark Task Complete/Incomplete**: Toggle the completion status of a task using its ID

## Quality Rules and Success Criteria
- Code must be readable, modular, and aligned with clean architecture principles.
- No deeply nested logic; functions should be simple and focused.
- Meaningful variable, function, and file names.
- Clear separation of concerns between components.
- Invalid input must be handled gracefully.
- Errors must not crash the application.
- All five core features work correctly.
- The application runs without errors.
- Code follows clean structure and principles.
- All work is documented in specs-history.
- The console app can be demonstrated end-to-end.

## Project Structure Requirements
- CONSTITUTION.md (this file)
- /specs-history/ folder containing all specification files
- /src/ folder containing Python source code
- README.md with setup and usage instructions
- CLAUDE.md with instructions for Claude Code usage

## Governance
Specifications govern behavior. AI accelerates execution. Architecture remains intentional.

**Version**: 1.1.0 | **Ratified**: 2025-12-29 | **Last Amended**: 2025-12-30