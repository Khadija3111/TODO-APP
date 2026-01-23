<!-- SYNC IMPACT REPORT -->
<!-- Version Change: 2.0.0 → 3.0.0 -->
<!-- Modified Principles: Complete overhaul for Phase III Todo AI Chatbot with MCP -->
<!-- Added Sections: All new principles for AI Chatbot, MCP server, stateless design, tool-centric behavior -->
<!-- Removed Sections: Legacy CLI features section (replaced with new AI Chatbot standards) -->
<!-- Templates Requiring Updates: -->
<!-- - .specify/templates/plan-template.md: ✅ Updated -->
<!-- - .specify/templates/spec-template.md: ✅ Updated -->
<!-- - .specify/templates/tasks-template.md: ✅ Updated -->
<!-- Follow-up TODOs: None -->

# Project Constitution: Phase III – Todo AI Chatbot with MCP

## Version Information
- **Version**: v3.0.0
- **Ratification Date**: 2026-01-17
- **Last Amended**: 2026-01-17

## Core Principles

### Principle 1: End-to-End Integration with Existing Stack
The system MUST integrate seamlessly with the existing Phase II backend (FastAPI + SQLModel + Neon PostgreSQL) and frontend (Next.js) without breaking existing functionality.

**Rationale**: Maintaining backward compatibility preserves user investment and reduces deployment risk.

### Principle 2: Stateless Server Design
Every request MUST be independently reproducible from the database. No server-side session state is allowed.

**Rationale**: Stateless design ensures scalability, resilience, and simplifies deployment strategies.

### Principle 3: Tool-Centric AI Behavior
All task changes MUST go through MCP tools, never assumed or simulated by the AI agent.

**Rationale**: Direct tool usage ensures data consistency and provides a clear audit trail for all operations.

### Principle 4: User-Friendly Natural Language Interaction
The AI agent MUST provide clear, user-friendly natural language interaction focused on task management and account awareness.

**Rationale**: Accessibility and ease of use drive user adoption and satisfaction.

### Principle 5: Safety and Graceful Error Handling
All agent actions MUST incorporate safety, correctness, and graceful error handling.

**Rationale**: Robust error handling prevents system failures and provides better user experience during exceptional conditions.

## Key Standards

### Task Management Capabilities
The chatbot MUST fully support:
- Task creation, listing (all/pending/completed), completion, deletion, and updating via MCP tools
- Conversation context reconstruction from `Conversation` and `Message` tables
- Multi-turn dialogues where the agent remembers prior turns via DB, not process memory
- Awareness of the authenticated user (user_id/email) as given by the backend

### Backend Integration Standards
The system MUST:
- Use the existing FastAPI app and Neon PostgreSQL, extending it with:
  - `Task(user_id, id, title, description, completed, created_at, updated_at)`
  - `Conversation(user_id, id, created_at, updated_at)`
  - `Message(user_id, id, conversation_id, role, content, created_at)`
- Implement `POST /api/{user_id}/chat` that:
  - Accepts `{ conversation_id?, message }`
  - Loads history from DB, appends the new message, invokes the AI agent, stores the assistant reply, and returns `{ conversation_id, response, tool_calls }`
  - Remains stateless across requests (all context comes from DB)

### MCP Server and Tools Standards
The system MUST:
- Use the official MCP SDK to expose the following tools against Neon DB via SQLModel:
  - `add_task(user_id, title, description?)`
  - `list_tasks(user_id, status?)` with `status ∈ {"all","pending","completed"}`
  - `complete_task(user_id, task_id)`
  - `delete_task(user_id, task_id)`
  - `update_task(user_id, task_id, title?, description?)`
- All tools MUST:
  - Be stateless (no in-memory user state)
  - Scope all queries by `user_id`
  - Return clear, structured results (task_id, status, title, and error messages where needed)

### AI Framework and Provider Standards
The system MUST:
- Use Cohere as the LLM provider for the chatbot while orchestrating tools through the OpenAI Agents SDK
- All agent behavior MUST be expressible as:
  - System/constitution prompt
  - Conversation history from DB
  - Tool definitions from the MCP server

### Frontend Integration Standards
The system MUST:
- Integrate the chatbot into the existing Next.js frontend using ChatKit
- ChatKit MUST send and receive messages through the FastAPI `/api/{user_id}/chat` endpoint, not directly to a model provider
- The frontend MUST manage `conversation_id` across turns and include the authenticated `user_id` in requests

## Agent Behavior Constraints

### Tool Usage Rules
The agent MUST:
- Use `add_task` when the user talks about adding/creating/remembering something or expresses a desire to not forget an item
- Use `list_tasks` when the user asks to see/show/list tasks or asks "what's pending/completed/all my tasks"
- Use `complete_task` when the user says a task is done/finished/complete or explicitly asks to mark a task complete
- Use `delete_task` when the user asks to remove/delete/cancel a task; if they refer by name ("the meeting task"), fetch tasks via `list_tasks` and disambiguate before deleting
- Use `update_task` when the user wants to rename/change/update a task's title or description
- NEVER claim that a task has been created, updated, completed, or deleted without actually calling the corresponding tool and checking its result

### Conversation Management Rules
The agent MUST:
- Treat each request as stateless on the server: rely completely on the `Conversation` + `Message` records sent by the backend for context
- When the user references prior turns ("that task", "the one we just created"), resolve references by:
  - Reading provided history
  - Calling `list_tasks` if needed to match titles/IDs
- Store every user and assistant message to DB via the backend's logic so conversations can be resumed after server restarts

### User Identity Rules
The agent MUST:
- When the user asks "what email am I logged in with?" or similar, answer using the authenticated identity (user_id/email) provided in system or request context from the backend
- NEVER invent or guess an email or user_id; if no identity info is provided, explicitly say that it is not available in this context

## Interaction Style Guidelines

### Response Style
The agent SHOULD:
- Provide short, clear, action-oriented responses that confirm what happened
- When performing an operation, explicitly mention:
  - Task ID and title for creations, updates, completions, and deletions
- When listing tasks, format them in a readable way (e.g., bullet list with ID, title, and completion status)
- Ask clarifying questions when:
  - Multiple tasks match a vague description
  - The user's intent is ambiguous (e.g., "remove the last one" without context)

## Implementation Workflow Standards

### Agentic Dev Stack Compliance
All development MUST follow the Agentic Dev Stack workflow:
1. Write or refine a spec for the requested change or component
2. Generate a step-by-step implementation plan
3. Break the plan into small tasks suitable for an automated coding agent
4. Implement via automated coding (no manual coding by the human user)

### Project Structure Compliance
All implementations MUST fit cleanly into the existing project structure (frontend `/frontend`, backend `/backend`, specs in `/specs`, migrations, and README updates)

## Constraints

### Integration Constraints
The system MUST:
- Integrate cleanly into existing Phase II code:
  - No breaking of existing Next.js pages or FastAPI endpoints unless explicitly agreed
  - Database migrations must be additive and backwards compatible where possible

### Reliability Constraints
The system MUST:
- MCP tools and chat endpoint tolerate failures gracefully (DB errors, missing tasks, invalid IDs) and surface user-friendly error messages
- All configuration for providers (Cohere, OpenAI Agents SDK, domain allowlist keys) must be handled via environment variables and documented in README

## Success Criteria

### Backend Functionality
The system MUST enable:
- A working chatbot that, through the FastAPI `/api/{user_id}/chat` endpoint, can:
  - Add, list, complete, delete, and update tasks for the authenticated user using MCP tools
  - Maintain and resume conversation context purely from the database (stateless server)
  - Correctly answer which email/account is in use when that info is available from the backend

### Frontend Functionality
The system MUST enable:
- The Next.js + ChatKit frontend to:
  - Start a new conversation and continue existing ones using `conversation_id`
  - Display tool-driven changes (task lists, confirmations) clearly

### Resilience Criteria
The system MUST:
- Be able to recover from server restarts without losing any conversation data or task state

## Governance

### Amendment Procedure
Changes to this constitution require:

- Proposal with clear justification
- Review by project stakeholders
- Approval by majority consensus
- Documentation of changes in the SYNC IMPACT REPORT section

### Versioning Policy
- MAJOR: Backward incompatible governance/principle removals or redefinitions
- MINOR: New principle/section added or materially expanded guidance
- PATCH: Clarifications, wording, typo fixes, non-semantic refinements

### Compliance Review
Regular compliance reviews SHOULD occur to ensure ongoing adherence to constitutional principles.

## Configuration

### Cohere API Key
The system MUST use the provided Cohere API key for LLM functionality:
```

```