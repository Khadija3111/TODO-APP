---
id: constitution-2026-01-17-amend-v3-0-0
title: Amend Constitution Phase III Todo Chatbot v3.0.0
date: 2026-01-17
stage: constitution
author: Claude
version: 1.0.0
---

# Amend Constitution Phase III Todo Chatbot v3.0.0

## Summary
Updated the project constitution to reflect the requirements for Phase III - Todo AI Chatbot with MCP, integrating with the existing Next.js + FastAPI + Neon stack using Cohere + OpenAI Agents SDK.

## Original Prompt
```
Project: Phase III – Todo AI Chatbot with MCP, Existing Next.js + FastAPI + Neon Stack, using Cohere + OpenAI Agents SDK

Core principles:
- End-to-end integration with existing Phase II backend (FastAPI + SQLModel + Neon PostgreSQL) and frontend (Next.js)
- Strict stateless server design: every request is independently reproducible from the database
- Tool‑centric AI behavior: all task changes go through MCP tools, never assumed
- Clear, user-friendly natural language interaction focused on task management and account awareness
- Safety, correctness, and graceful error handling in all agent actions

Key standards:
- The chatbot must fully support:
  - Task creation, listing (all/pending/completed), completion, deletion, and updating via MCP tools
  - Conversation context reconstruction from `Conversation` and `Message` tables
  - Multi-turn dialogues where the agent remembers prior turns via DB, not process memory
  - Awareness of the authenticated user (user_id/email) as given by the backend
- Backend integration:
  - Use the existing FastAPI app and Neon PostgreSQL, extending it with:
    - `Task(user_id, id, title, description, completed, created_at, updated_at)`
    - `Conversation(user_id, id, created_at, updated_at)`
    - `Message(user_id, id, conversation_id, role, content, created_at)`
  - Implement `POST /api/{user_id}/chat` that:
    - Accepts `{ conversation_id?, message }`
    - Loads history from DB, appends the new message, invokes the AI agent, stores the assistant reply, and returns `{ conversation_id, response, tool_calls }`
    - Remains stateless across requests (all context comes from DB)
- MCP server and tools:
  - Use the official MCP SDK to expose the following tools against Neon DB via SQLModel:
    - `add_task(user_id, title, description?)`
    - `list_tasks(user_id, status?)` with `status ∈ {"all","pending","completed"}`
    - `complete_task(user_id, task_id)`
    - `delete_task(user_id, task_id)`
    - `update_task(user_id, task_id, title?, description?)`
  - All tools must:
    - Be stateless (no in‑memory user state)
    - Scope all queries by `user_id`
    - Return clear, structured results (task_id, status, title, and error messages where needed)
- AI framework and providers:
  - Use Cohere as the LLM provider for the chatbot while orchestrating tools through the OpenAI Agents SDK, configured via a Cohere‑compatible API key or bridge layer as defined in the project.
  - All agent behavior must be expressible as:
    - System/constitution prompt
    - Conversation history from DB
    - Tool definitions from the MCP server
- Frontend / ChatKit:
  - Integrate the chatbot into the existing Next.js frontend using ChatKit.
  - ChatKit must send and receive messages through the FastAPI `/api/{user_id}/chat` endpoint, not directly to a model provider.
  - The frontend must manage `conversation_id` across turns and include the authenticated `user_id` in requests.

Agent behavior constraints:
- Tool usage rules:
  - Use `add_task` when the user talks about adding/creating/remembering something or expresses a desire to not forget an item.
  - Use `list_tasks` when the user asks to see/show/list tasks or asks "what's pending/completed/all my tasks".
  - Use `complete_task` when the user says a task is done/finished/complete or explicitly asks to mark a task complete.
  - Use `delete_task` when the user asks to remove/delete/cancel a task; if they refer by name ("the meeting task"), fetch tasks via `list_tasks` and disambiguate before deleting.
  - Use `update_task` when the user wants to rename/change/update a task's title or description.
  - Never claim that a task has been created, updated, completed, or deleted without actually calling the corresponding tool and checking its result.
- Conversation management:
  - Treat each request as stateless on the server: rely completely on the `Conversation` + `Message` records sent by the backend for context.
  - When the user references prior turns ("that task", "the one we just created"), resolve references by:
    - Reading provided history
    - Calling `list_tasks` if needed to match titles/IDs
  - Store every user and assistant message to DB via the backend's logic so conversations can be resumed after server restarts.
- User identity and email:
  - When the user asks "what email am I logged in with?" or similar, answer using the authenticated identity (user_id/email) provided in system or request context from the backend.
  - Never invent or guess an email or user_id; if no identity info is provided, explicitly say that it is not available in this context.

Interaction style:
- Short, clear, action‑oriented responses that confirm what happened.
- When performing an operation, explicitly mention:
  - Task ID and title for creations, updates, completions, and deletions.
- When listing tasks, format them in a readable way (e.g., bullet list with ID, title, and completion status).
- Ask clarifying questions when:
  - Multiple tasks match a vague description
  - The user's intent is ambiguous (e.g., "remove the last one" without context)

Implementation workflow standards:
- Follow the Agentic Dev Stack workflow at all times:
  1) Write or refine a spec for the requested change or component.
  2) Generate a step‑by‑step implementation plan.
  3) Break the plan into small tasks suitable for an automated coding agent.
  4) Implement via automated coding (no manual coding by the human user).
- Ensure each generated plan fits cleanly into the existing project structure (frontend `/frontend`, backend `/backend`, specs in `/specs`, migrations, and README updates).

Constraints:
- Must integrate cleanly into existing Phase II code:
  - No breaking of existing Next.js pages or FastAPI endpoints unless explicitly agreed.
  - Database migrations must be additive and backwards compatible where possible.
- MCP tools and chat endpoint must tolerate failures gracefully (DB errors, missing tasks, invalid IDs) and surface user‑friendly error messages.
- All configuration for providers (Cohere, OpenAI Agents SDK, domain allowlist keys) must be handled via environment variables and documented in README.

Success criteria:
- A working chatbot that, through the FastAPI `/api/{user_id}/chat` endpoint, can:
  - Add, list, complete, delete, and update tasks for the authenticated user using MCP tools.
  - Maintain and resume conversation context purely from the database (stateless server).
  - Correctly answer which email/account is in use when that info is available from the backend.
- The Next.js + ChatKit frontend can:
  - Start a new conversation and continue existing ones using `conversation_id`.
  - Display tool‑driven changes (task lists, confirmations) clearly.
- The system can recover from server restarts without losing any conversation data or task state. 
```

## Response Summary
Updated the project constitution file (.specify/memory/constitution.md) from version 2.0.0 to 3.0.0 to reflect the requirements for Phase III Todo AI Chatbot with MCP. The new constitution includes:

- Core principles for end-to-end integration, stateless server design, tool-centric AI behavior, user-friendly interaction, and safety/error handling
- Key standards for task management, backend integration, MCP server, AI framework, and frontend integration
- Agent behavior constraints for tool usage, conversation management, and user identity handling
- Implementation workflow standards following the Agentic Dev Stack
- Constraints for integration and reliability
- Success criteria for backend, frontend, and resilience requirements
- Configuration including the provided Cohere API key

## Changes Made
- Updated constitution version from 2.0.0 to 3.0.0
- Completely revised principles to focus on Phase III requirements
- Added detailed standards for MCP server and AI integration
- Included specific tool signatures and behaviors
- Incorporated Cohere API key in configuration section