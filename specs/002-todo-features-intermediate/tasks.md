# Implementation Tasks: Intermediate-Level Features for Console-Based Todo App

## Feature Overview
Implementing intermediate-level features (Priorities, Tags, Search, Filter, Sort) for the console-based Todo app.

## Phase 1: Setup Tasks
- [x] T001 Create project structure per implementation plan in src/utils/
- [x] T002 Set up development environment with required dependencies
- [x] T003 Initialize configuration directory ~/.todo/ if not exists

## Phase 2: Foundational Tasks
- [x] T004 Extend Task model with priority and tags fields in src/models/task.py
- [x] T005 Create config service for persistent preferences in src/services/config_service.py
- [x] T006 Update TaskStore to handle new priority and tags fields in src/services/task_store.py
- [x] T007 Create utility modules (filters, search, sorters) in src/utils/

## Phase 3: [US1] Prioritize and Tag Tasks
- [x] T008 [US1] Update CLI interface to accept priority flags (--priority/-p) in src/cli/cli_interface.py
- [x] T009 [US1] Update CLI interface to accept tags flags (--tags/-t) in src/cli/cli_interface.py
- [x] T010 [US1] Implement priority and tags validation in src/models/task.py
- [x] T011 [US1] Update task creation flow to handle priority and tags in src/services/task_store.py
- [x] T012 [US1] Update task update flow to handle priority and tags in src/services/task_store.py
- [x] T013 [US1] Update task display to show priority and tags in src/cli/cli_interface.py
- [x] T014 [US1] Test priority and tags functionality with manual verification

## Phase 4: [US2] Search Tasks by Content
- [x] T015 [US2] Create search utility functions in src/utils/search.py
- [x] T016 [US2] Implement case-insensitive partial matching algorithm
- [x] T017 [US2] Add search command to CLI interface in src/cli/cli_interface.py
- [x] T018 [US2] Integrate search functionality with task store in src/services/task_store.py
- [x] T019 [US2] Test search functionality with various keywords and scenarios
- [x] T020 [US2] Verify "todo search meet" returns tasks containing "meeting"

## Phase 5: [US3] Filter Tasks by Attributes
- [x] T021 [US3] Create filter utility functions in src/utils/filters.py
- [x] T022 [US3] Implement status, priority, and tags filtering logic
- [x] T023 [US3] Add filter options to CLI list command in src/cli/cli_interface.py
- [x] T024 [US3] Integrate filter functionality with task store in src/services/task_store.py
- [x] T025 [US3] Test filter combinations (status + priority, status + tags, etc.)
- [x] T026 [US3] Verify filters work in any combination as specified

## Phase 6: [US4] Sort Tasks by Various Criteria
- [x] T027 [US4] Create sort utility functions in src/utils/sorters.py
- [x] T028 [US4] Implement sorting by due date, priority, alphabetical, creation date
- [x] T029 [US4] Add sort options to CLI list command in src/cli/cli_interface.py
- [x] T030 [US4] Integrate sort functionality with task store in src/services/task_store.py
- [x] T031 [US4] Implement config persistence for sort preferences in src/services/config_service.py
- [x] T032 [US4] Test sort functionality with all fields and ascending/descending

## Phase 7: [US5] Accessible Command-Line Interface
- [x] T033 [US5] Update help text to include all new flags and examples in src/cli/cli_interface.py
- [x] T034 [US5] Implement ANSI color support for status display in src/cli/renderers.py
- [x] T035 [US5] Add --no-color flag for color-disabled environments in src/cli/cli_interface.py
- [x] T036 [US5] Improve error messages with descriptive text and proper exit codes
- [x] T037 [US5] Test keyboard-driven navigation and accessibility features

## Phase 8: Polish & Cross-Cutting Concerns
- [x] T038 Update README with new usage examples and feature documentation
- [x] T039 Write unit tests for all new utility functions (≥80% coverage)
- [x] T040 Write integration tests for CLI commands and workflows
- [x] T041 Performance test with 500 tasks to ensure ≤100ms operations
- [x] T042 Document all technical decisions in DECISIONS.md
- [x] T043 Create architecture diagram in architecture.txt
- [x] T044 Final integration testing of all features together
- [x] T045 Code review and cleanup of implementation

## Dependencies
- US1 (Prioritize and Tag Tasks) must be completed before US3 (Filter Tasks) and US4 (Sort Tasks) can be fully tested
- Foundational Tasks (T004-T007) must be completed before any user story tasks

## Parallel Execution Opportunities
- [P] T008, T009: Priority and tags CLI flags can be implemented in parallel
- [P] T015, T021, T027: Utility modules (search, filters, sorters) can be developed in parallel
- [P] T017, T023, T029: CLI command additions can be implemented in parallel after foundational work

## Implementation Strategy
- MVP approach: Focus on US1 (Priority and Tags) as the foundation for other features
- Incremental delivery: Each user story phase delivers independently testable functionality
- Test-driven development: Validate each feature as it's implemented