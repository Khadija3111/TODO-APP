# Implementation Plan: AI Chatbot with MCP Integration

**Feature**: 003-ai-chatbot-mcp
**Created**: 2026-01-17
**Status**: Draft
**Based on**: specs/003-ai-chatbot-mcp/spec.md

## Overview and Goals of Phase III

The goal of Phase III is to enhance the existing Todo application with an AI-powered chatbot that enables natural language task management. The chatbot will interact with tasks through an MCP server, using Cohere as the LLM orchestrated via the OpenAI Agents SDK. This will provide users with a conversational interface to add, list, update, complete, and delete tasks while maintaining seamless integration with the existing Next.js frontend and FastAPI backend.

### High-Level Architecture

```
┌─────────────────┐    ┌──────────────────────┐    ┌─────────────────┐
│   Next.js       │    │     FastAPI         │    │   Neon          │
│   Frontend      │◄──►│     Backend         │◄──►│   PostgreSQL    │
│                 │    │                     │    │                 │
│  ┌───────────┐  │    │  ┌────────────────┐ │    │  ┌───────────┐  │
│  │ChatKit    │  │    │  │/api/{user_id}/ │ │    │  │Task       │  │
│  │Panel      │◄─┼────┼──┤chat endpoint   │ │    │  │Table      │  │
│  │           │  │    │  │                │ │    │  │           │  │
│  │Chatbot    │  │    │  │  ┌───────────┐ │ │    │  │Conversation│ │
│  │Icon       │  │    │  │  │MCP Server │ │ │    │  │Table      │  │
│  │           │  │    │  │  │           │ │ │    │  │           │  │
│  └───────────┘  │    │  │  │Tools:     │ │ │    │  │Message    │  │
│                 │    │  │  │add_task,   │ │ │    │  │Table      │  │
│                 │    │  │  │list_tasks, │ │ │    │  │           │  │
│                 │    │  │  │etc.        │ │ │    │  └───────────┘  │
└─────────────────┘    │  │  └───────────┘ │ │    │                 │
                       │  └────────────────┘ │    └─────────────────┘
                       │                     │
                       │  ┌────────────────┐ │
                       │  │OpenAI Agents │ │ │
                       │  │SDK            │ │ │
                       │  │               │ │ │
                       │  │  ┌─────────┐  │ │ │
                       │  │  │Cohere   │  │ │ │
                       │  │  │LLM      │  │ │ │
                       │  │  └─────────┘  │ │ │
                       │  └────────────────┘ │ │
                       └──────────────────────┘
```

## Technical Approach

### Foundation Phase
1. **Confirm existing Phase II structure**
   - Verify current Next.js frontend setup
   - Confirm FastAPI backend with SQLModel and Neon integration
   - Review existing Task model and authentication system

2. **Database model adjustments**
   - Extend Task model with user_id scoping if not already present
   - Add Conversation and Message models for chat history
   - Create necessary database migrations

3. **Define MCP tool interfaces**
   - Specify tool signatures and expected return types
   - Plan error handling and response structures

### Backend & MCP Phase
1. **Implement MCP server**
   - Set up MCP server with official SDK
   - Implement add_task, list_tasks, complete_task, delete_task, update_task tools
   - Connect tools to Neon DB via SQLModel with proper user scoping

2. **Implement chat endpoint**
   - Create POST /api/{user_id}/chat endpoint in FastAPI
   - Implement conversation history reconstruction from DB
   - Store user and assistant messages in database
   - Wire up OpenAI Agents SDK with Cohere configuration

3. **Configuration and environment handling**
   - Set up Cohere API key management
   - Configure OpenAI Agents SDK for Cohere compatibility

### Agent & Prompts Phase
1. **Apply Phase III constitution**
   - Implement agent instructions based on project constitution
   - Define tool usage rules and error handling

2. **Identity awareness**
   - Implement user identity propagation from auth to agent context
   - Handle email queries appropriately

### Frontend & ChatKit Phase
1. **UI Integration**
   - Add chatbot icon to existing Next.js UI
   - Implement ChatKit panel integration
   - Handle conversation_id lifecycle

2. **Endpoint Wiring**
   - Connect ChatKit to FastAPI chat endpoint
   - Manage user_id and conversation_id in frontend

### Validation & Polish Phase
1. **Testing implementation**
   - Unit tests for MCP tools
   - Integration tests for chat endpoint
   - Scenario tests for natural language commands

2. **Documentation updates**
   - Update README with new architecture
   - Document environment variables and setup

## Implementation Steps

### Step 1: Foundation Setup
- [ ] Analyze existing Phase II codebase structure
- [ ] Verify database schema and authentication setup
- [ ] Confirm Task model includes user_id for scoping
- [ ] Add Conversation and Message SQLModel classes
- [ ] Create and run database migrations

### Step 2: MCP Server Development
- [ ] Install and configure official MCP SDK
- [ ] Implement add_task(user_id, title, description?) tool
- [ ] Implement list_tasks(user_id, status?) tool with status filtering
- [ ] Implement complete_task(user_id, task_id) tool
- [ ] Implement delete_task(user_id, task_id) tool
- [ ] Implement update_task(user_id, task_id, title?, description?) tool
- [ ] Add error handling and structured responses to all tools
- [ ] Test MCP tools directly with database operations

### Step 3: Backend Chat Endpoint
- [ ] Create /api/{user_id}/chat endpoint in FastAPI
- [ ] Implement conversation history loading from DB
- [ ] Add new user message to database
- [ ] Configure OpenAI Agents SDK with Cohere
- [ ] Call agent with tools from MCP server
- [ ] Store assistant response in database
- [ ] Return structured response with conversation_id and tool_calls

### Step 4: Agent Configuration
- [ ] Set up Cohere API key in environment variables
- [ ] Configure OpenAI Agents SDK to work with Cohere
- [ ] Apply Phase III constitution as system prompt
- [ ] Implement tool usage rules and natural language mappings
- [ ] Add user identity awareness to agent context

### Step 5: Frontend Integration
- [ ] Add chatbot icon to existing Next.js layout
- [ ] Implement ChatKit panel component
- [ ] Connect ChatKit to backend chat endpoint
- [ ] Handle conversation_id lifecycle in frontend
- [ ] Format task lists and responses appropriately in UI

### Step 6: Testing and Validation
- [ ] Write unit tests for MCP tools
- [ ] Create integration tests for chat endpoint
- [ ] Test stateless behavior after server restarts
- [ ] Validate natural language command scenarios
- [ ] Verify user identity handling
- [ ] Test error handling and graceful failures

## Risk Mitigation

- **API Compatibility**: Carefully configure OpenAI Agents SDK to work with Cohere's API
- **Statelessness**: Ensure all conversation state is stored in DB, not memory
- **Security**: Validate all user inputs and maintain proper user_id scoping
- **Error Handling**: Implement comprehensive error handling with user-friendly messages

## Success Criteria Validation

- [ ] Natural language task management works reliably
- [ ] Conversations persist correctly across server restarts
- [ ] User data is properly isolated by user_id
- [ ] All Phase III success criteria are met
- [ ] Existing Phase II functionality remains intact