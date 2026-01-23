---
id: ai-chatbot-mcp-plan-2026-01-17
title: Create Plan AI Chatbot MCP
date: 2026-01-17
stage: plan
author: Claude
version: 1.0.0
---

# Create Plan AI Chatbot MCP

## Summary
Created the implementation plan for the AI Chatbot with MCP integration, detailing the technical approach and phased implementation for adding an AI-powered chatbot interface to the existing Todo application using Cohere, OpenAI Agents SDK, and MCP server integration.

## Original Prompt
```
Phase III – Todo AI Chatbot with MCP, Cohere, OpenAI Agents SDK, and Existing Next.js + FastAPI + Neon Stack

Create:

High-level architecture and data flow sketch connecting:

Existing Next.js frontend (with new chatbot icon and ChatKit panel)

FastAPI backend with /api/{user_id}/chat endpoint

MCP server exposing todo tools (add/list/complete/delete/update)

Neon PostgreSQL with Task, Conversation, Message tables

Cohere LLM accessed through OpenAI Agents SDK

Detailed section structure for the project plan:

Overview and goals of Phase III

Backend changes (chat endpoint, Agents SDK integration, MCP server)

Frontend changes (ChatKit UI, chatbot icon, wiring to chat endpoint)

Data and state model (DB schemas, stateless behavior)

Agent design (constitution, tool usage rules, error handling, identity awareness)

Deployment, environment variables, and domain allowlist configuration

Implementation approach for each area:

Backend: additive integration into existing FastAPI app and Neon DB, new migrations only.

MCP: tool definitions and DB access patterns for user-scoped tasks.

Agents: configuring OpenAI Agents SDK to call Cohere via compatible API key and models.

Frontend: ChatKit wiring, conversation_id handling, UI states.

Quality validation plan for:

Functional flows (add/list/update/complete/delete tasks via chat).

Statelessness (restarting backend doesn't break ongoing conversations).

Correct tool selection and safe behavior for ambiguous instructions.

Proper handling of user identity/email questions.

Decisions needing documentation:

LLM/Agents layer:

Which Cohere model to use and how it is mapped/configured inside the Agents SDK.

How to manage model/endpoint configuration via environment variables.

MCP architecture:

Whether MCP server runs inside the FastAPI process or as a separate process/service.

Error-handling strategy and response schema for each tool.

Chat endpoint design:

Exact shape of request/response JSON for /api/{user_id}/chat.

How to represent tool_calls in responses (for debugging vs. user-facing UI).

Conversation and identity model:

How user_id and email are propagated from auth → backend → agent.

How conversations are scoped (per user, per device, etc.).

Frontend integration:

Where the chatbot icon and panel live in the existing UI.

How the frontend manages conversation_id and persists it (in-memory vs storage).

Security and configuration:

How to store and load Cohere API key and any Agents SDK settings.

Domain allowlist and domain key configuration for ChatKit.

Testing strategy:

Define validation checks tied directly to Phase III success criteria:

For each tool (add_task, list_tasks, complete_task, delete_task, update_task):

Unit tests verifying correct DB changes, user_id scoping, and error paths.

For /api/{user_id}/chat:

Integration tests that:

Simulate multi-turn conversations and verify DB messages.

Confirm behavior after process restart (statelessness via DB).

Validate proper propagation of conversation_id.

For agent behavior:

Scenario tests for natural-language commands (add, list, complete, delete, update, "what email am I logged in with?", ambiguous task names).

Checks that agent always uses tools instead of hallucinating state changes.

Frontend tests:

Verify that the chatbot icon opens the panel and sends/receives messages correctly.

Ensure conversation_id is preserved across turns in the UI.

Non-functional checks:

Ensure environment variables are required and validated on startup.

Confirm that errors are surfaced as friendly messages without leaking secrets.

Technical details:

Organize the implementation and planning work in phases:

Foundation

Confirm existing Phase II structure (frontend/backend/db).

Add/adjust DB models and migrations for Conversation and Message if needed.

Define MCP tool interfaces and schemas.

Backend & MCP

Implement and register the MCP server and tools against Neon via SQLModel.

Implement /api/{user_id}/chat, including conversation reconstruction and Agents SDK wiring to Cohere.

Add configuration and env handling for Cohere + Agents SDK.

Agent & Prompts

Apply the Phase III constitution and specify agent instructions for todo behavior, identity awareness, and error handling.

Test tool-calling behavior with representative inputs.

Frontend & ChatKit

Add chatbot icon and ChatKit panel to Next.js.

Wire ChatKit to the FastAPI chat endpoint, including conversation_id and user_id.

Validation & Polish

Implement test suites (unit + integration).

Run manual scenario tests (task flows, restarts, identity questions).

Update README and /specs with final architecture and usage instructions.
```

## Response Summary
Generated a comprehensive implementation plan for the AI Chatbot with MCP integration, including:

- High-level architecture diagram showing the system components
- Phased implementation approach (Foundation, Backend & MCP, Agent & Prompts, Frontend & ChatKit, Validation & Polish)
- Detailed implementation steps organized by phase
- Risk mitigation strategies
- Success criteria validation checklist

## Changes Made
- Created plan file at specs/003-ai-chatbot-mcp/plan.md
- Organized implementation in logical phases with specific tasks
- Included architecture diagram and technical approach
- Added validation and risk mitigation strategies