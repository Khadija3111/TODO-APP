---
description: "Task list for AI Chatbot with MCP Integration feature implementation"
---

# Tasks: AI Chatbot with MCP Integration

**Input**: Design documents from `/specs/003-ai-chatbot-mcp/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- **Backend**: `backend/` with `models/`, `services/`, `api/`, `utils/`
- **Frontend**: `frontend/` with `components/`, `pages/`, `utils/`
- Paths adjusted based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Install and configure MCP SDK in backend
- [x] T002 [P] Add Cohere and OpenAI Agents SDK dependencies to backend
- [x] T003 [P] Update environment variables configuration for Cohere API key

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Create Conversation and Message SQLModel classes in backend/models/conversation.py
- [x] T005 Create database migrations for Conversation and Message tables
- [x] T006 [P] Implement database utility functions for conversation management in backend/utils/database.py
- [x] T007 Set up basic MCP server structure in backend/mcp/server.py
- [x] T008 Configure environment variables validation for Cohere integration

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Basic Chatbot Task Management (Priority: P1) 🎯 MVP

**Goal**: Enable users to interact with an AI chatbot that can manage todo tasks using natural language commands to add, list, update, complete, and delete tasks.

**Independent Test**: Can engage with the chatbot through natural language commands like "add a task to buy groceries", "show me pending tasks", "mark task 1 as complete", and verify that tasks are properly created, listed, updated, and deleted in the database.

### Implementation for User Story 1

- [x] T009 [P] [US1] Implement add_task MCP tool in backend/mcp/tools/task_operations.py
- [x] T010 [P] [US1] Implement list_tasks MCP tool in backend/mcp/tools/task_operations.py
- [x] T011 [P] [US1] Implement complete_task MCP tool in backend/mcp/tools/task_operations.py
- [x] T012 [P] [US1] Implement delete_task MCP tool in backend/mcp/tools/task_operations.py
- [x] T013 [P] [US1] Implement update_task MCP tool in backend/mcp/tools/task_operations.py
- [x] T014 [US1] Register MCP tools with the MCP server
- [x] T015 [US1] Create basic agent configuration with Cohere integration in backend/agents/config.py
- [x] T016 [US1] Test basic task operations through MCP tools

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - MCP Server Integration (Priority: P1)

**Goal**: Ensure the AI chatbot interacts with tasks through an MCP server that exposes standardized tools for reliable task operations while maintaining data consistency.

**Independent Test**: Verify that the MCP server exposes the required tools (add_task, list_tasks, complete_task, delete_task, update_task) and that they properly interact with the Neon PostgreSQL database using SQLModel.

### Implementation for User Story 2

- [x] T017 [P] [US2] Enhance MCP tools with proper error handling and structured JSON responses
- [x] T018 [P] [US2] Add user_id scoping validation to all MCP tools
- [x] T019 [US2] Implement tool response formatting with task_id, status, title, and error messages
- [x] T020 [US2] Test MCP tools directly with database operations
- [x] T021 [US2] Validate user_id scoping in all MCP operations

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Stateless Chat Interface (Priority: P2)

**Goal**: Enable conversations with the AI chatbot that maintain context across multiple messages, allowing for natural, multi-turn interactions without losing conversation history.

**Independent Test**: Start a conversation, perform multiple task operations across several messages, and verify that the conversation context is maintained and accessible in the database.

### Implementation for User Story 3

- [x] T022 [P] [US3] Create POST /api/{user_id}/chat endpoint in backend/api/chat.py
- [x] T023 [P] [US3] Implement conversation history loading from DB in backend/services/conversation_service.py
- [x] T024 [US3] Add user message storage to database in backend/services/message_service.py
- [x] T025 [US3] Implement assistant response storage to database in backend/services/message_service.py
- [x] T026 [US3] Integrate OpenAI Agents SDK with Cohere and MCP tools in backend/agents/chat_agent.py
- [x] T027 [US3] Return structured response with conversation_id and tool_calls from chat endpoint
- [x] T028 [US3] Test multi-turn conversations and database persistence
- [x] T029 [US3] Validate stateless behavior after server restarts

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Frontend Chat Integration (Priority: P2)

**Goal**: Provide users with intuitive access to the AI chatbot through an interface in the existing Next.js application, allowing easy switching between traditional UI and AI-powered task management.

**Independent Test**: Click the chatbot icon in the UI, open the ChatKit panel, send messages to the backend endpoint, and receive responses with proper formatting of task information.

### Implementation for User Story 4

- [x] T030 [P] [US4] Add chatbot icon component to frontend in frontend/components/ChatbotIcon.jsx
- [x] T031 [P] [US4] Create ChatKit panel component in frontend/components/ChatPanel.jsx
- [x] T032 [US4] Implement API call to backend /api/{user_id}/chat endpoint in frontend/utils/api.js
- [x] T033 [US4] Handle conversation_id lifecycle in frontend state management
- [x] T034 [US4] Format task lists and responses in chat interface
- [x] T035 [US4] Integrate chat panel with existing Next.js layout
- [x] T036 [US4] Test frontend-backend communication

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: User Story 5 - Advanced Task Operations (Priority: P3)

**Goal**: Handle complex task operations like disambiguating task names and handling errors gracefully, allowing sophisticated task management without confusion.

**Independent Test**: Create multiple tasks with similar names, attempt to delete by name, and verify that the AI properly handles disambiguation and error cases.

### Implementation for User Story 5

- [x] T037 [P] [US5] Enhance agent with disambiguation logic for similar task names
- [x] T038 [P] [US5] Implement error handling for non-existent tasks in agent responses
- [x] T039 [US5] Add task name resolution logic to handle ambiguous requests
- [x] T040 [US5] Test disambiguation scenarios with multiple similar tasks
- [x] T041 [US5] Validate error message clarity for various failure cases

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T042 [P] Update README with AI Chatbot installation and setup instructions
- [x] T043 [P] Add environment variable documentation for Cohere and domain keys
- [x] T044 Add comprehensive error handling with user-friendly messages
- [x] T045 [P] Add logging for chat interactions and tool calls
- [x] T046 Security validation for user_id scoping and input sanitization
- [x] T047 Run end-to-end validation of all user stories

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Builds on US1/US2/US3 but should be independently testable
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - Builds on US1/US2/US3/US4 but should be independently testable

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tools for User Story 1 together:
Task: "Implement add_task MCP tool in backend/mcp/tools/task_operations.py"
Task: "Implement list_tasks MCP tool in backend/mcp/tools/task_operations.py"
Task: "Implement complete_task MCP tool in backend/mcp/tools/task_operations.py"
Task: "Implement delete_task MCP tool in backend/mcp/tools/task_operations.py"
Task: "Implement update_task MCP tool in backend/mcp/tools/task_operations.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence