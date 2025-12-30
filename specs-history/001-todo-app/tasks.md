# Implementation Tasks: Phase I – In-Memory Todo App

**Feature**: Phase I Todo Application
**Branch**: `001-todo-app`
**Created**: 2025-12-30
**Input**: Implementation plan from `/specs-history/001-todo-app/plan.md`

## Implementation Strategy

MVP first approach: Implement all 5 core features with minimal viable implementation, then add error handling and polish. Each feature represents an independently testable increment.

## Phase 1: Project Setup (Once)

Initialize project structure and dependencies as defined in the implementation plan.

- [X] T001 Create project directory structure: src/, src/models/, src/services/, src/cli/
- [X] T002 Create pyproject.toml with Python 3.13+ requirement
- [X] T003 Create README.md with setup and usage instructions
- [X] T004 Create main.py entry point file
- [X] T005 Create CLAUDE.md file with Claude Code usage instructions

## Phase 2: Core Domain & Storage (Shared)

Create the foundational components that all features depend on.

- [X] T006 [P] Create Task model with fields: id, title, description, completed
- [X] T007 [P] Create TaskStore with in-memory list
- [X] T008 [P] Implement auto-incrementing task ID
- [X] T009 [P] Implement basic input validation utilities
- [X] T010 Create base CLI helper for input/output

## Phase 3: Feature 1 — Add Task

Implement the core Add Task functionality as defined in the user story and functional requirements.

**Goal**: Allow users to add a new task with title and optional description, storing it in memory with unique ID and pending status.

**Independent Test Criteria**:
- User can enter a task title and optional description
- System creates task with unique ID and pending status
- System confirms task was added with its ID
- Invalid inputs are handled gracefully

**Tasks**:

- [X] T011 [P] [US1] Implement add_task function in TaskStore with validation
- [X] T012 [P] [US1] Create CLI function to prompt for task title in src/cli/cli_interface.py
- [X] T013 [P] [US1] Create CLI function to prompt for task description in src/cli/cli_interface.py
- [X] T014 [US1] Integrate add_task functionality with CLI interface
- [X] T015 [US1] Implement success message display after task creation
- [X] T016 [US1] Add error handling for empty title validation
- [X] T017 [US1] Add whitespace trimming for title and description inputs
- [X] T018 [US1] Test the complete add task flow from CLI to storage

## Phase 4: Feature 2 — View Tasks

Implement the View Tasks functionality to display all tasks.

**Goal**: Display all tasks with their ID, title, description, and completion status.

**Independent Test Criteria**:
- User can view all tasks in the system
- Each task shows ID, title, description, and status
- Appropriate message shown when no tasks exist

**Tasks**:

- [X] T019 [P] [US2] Implement get_all_tasks() in TaskStore
- [X] T020 [P] [US2] Create function to format task output in src/cli/cli_interface.py
- [X] T021 [US2] Show "No tasks found" when list is empty
- [X] T022 [US2] Implement CLI option to view tasks
- [X] T023 [US2] Format output with ID, title, description, and status

## Phase 5: Feature 3 — Update Task

Implement the Update Task functionality to modify existing tasks.

**Goal**: Allow users to update the title and/or description of an existing task by ID.

**Independent Test Criteria**:
- User can specify a task by ID
- User can update the title of a task
- User can update the description of a task
- System validates that the task exists before updating

**Tasks**:

- [X] T024 [P] [US3] Implement update_task(id, title, description) in TaskStore
- [X] T025 [P] [US3] Validate task ID exists in TaskStore
- [X] T026 [US3] Allow partial updates (title or description) in TaskStore
- [X] T027 [US3] Create CLI prompt for task ID in src/cli/cli_interface.py
- [X] T028 [US3] Create CLI prompt for updated fields in src/cli/cli_interface.py
- [X] T029 [US3] Display update confirmation to user

## Phase 6: Feature 4 — Delete Task

Implement the Delete Task functionality to remove tasks.

**Goal**: Allow users to delete a task by its ID.

**Independent Test Criteria**:
- User can specify a task by ID for deletion
- System validates that the task exists before deletion
- Task is removed from storage after deletion

**Tasks**:

- [X] T030 [P] [US4] Implement delete_task(id) in TaskStore
- [X] T031 [P] [US4] Validate task ID exists in TaskStore
- [X] T032 [US4] Create CLI prompt for task ID in src/cli/cli_interface.py
- [X] T033 [US4] Display delete confirmation to user

## Phase 7: Feature 5 — Toggle Completion

Implement the Toggle Task Completion functionality to change task status.

**Goal**: Allow users to toggle a task's completion status by its ID.

**Independent Test Criteria**:
- User can specify a task by ID to toggle status
- System validates that the task exists before toggling
- Task status changes from completed to pending or vice versa

**Tasks**:

- [X] T034 [P] [US5] Implement toggle_task_status(id) in TaskStore
- [X] T035 [P] [US5] Validate task ID exists in TaskStore
- [X] T036 [US5] Create CLI option to toggle status in src/cli/cli_interface.py
- [X] T037 [US5] Display updated status message to user

## Phase 8: Application Flow & Polish

Final implementation details and integration of all features.

- [X] T038 [P] Implement main menu loop in main.py with all 5 features
- [X] T039 [P] Add menu options for all 5 features
- [X] T040 Handle invalid menu input gracefully
- [X] T041 Implement clean exit option
- [X] T042 Manual end-to-end testing of all features
- [X] T043 Update README.md with all feature usage examples

## Dependencies

- All features require foundational components (Task model, TaskStore) to be implemented first
- CLI interface depends on Task model and TaskStore service
- Main application depends on all other components

## Parallel Execution Examples

**Parallel Tasks**:
- T019-T022: View tasks components can be developed simultaneously
- T024-T029: Update task components can be developed simultaneously
- T030-T033: Delete task components can be developed simultaneously
- T034-T037: Toggle completion components can be developed simultaneously

**Sequential Dependencies**:
- T001-T010 must complete before any feature tasks
- T006-T010 must complete before T011-T018 (Add Task)
- T006-T010 must complete before T019-T023 (View Tasks)
- T006-T010 must complete before T024-T029 (Update Task)
- T006-T010 must complete before T030-T033 (Delete Task)
- T006-T010 must complete before T034-T037 (Toggle Completion)