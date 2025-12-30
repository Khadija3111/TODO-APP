---
id: 1
title: "Add Project Constitution"
stage: constitution
date: 2025-12-29
surface: agent
model: Claude Sonnet 4.5
feature: "none"
branch: master
user: user
command: /sp.constitution
labels: ["constitution", "setup", "governance"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - ".specify/memory/constitution.md"
tests: []
---

# Add Project Constitution

## Prompt Text
```
# Project Constitution: Hackathon II – Spec-Driven Todo Evolution

## Project
Spec-Driven Development of a Todo system evolving from a CLI application to a distributed,
cloud-native, AI-powered platform.

## Core Principles
- **Spec-First Development**: All implementation must originate from written specifications.
- **Single Source of Truth**: Specs define behavior; code must conform to specs, not vice versa.
- **Incremental Evolution**: Each phase builds strictly on the previous phase without regressions.
- **Stateless & Scalable Design**: Systems must favor stateless services and externalized state.
- **AI-Augmented Engineering**: AI tools are used to reduce boilerplate, not architectural thinking.

## Key Standards
- All features must be explicitly defined in `/specs` before implementation.
- Claude Code must reference specs using `@specs/...` when generating or modifying code.
- Each phase must preserve backward functionality from earlier phases.
- API behavior must be deterministic, documented, and testable.
- Authentication and authorization must enforce strict user isolation.
- AI agents may only act through defined MCP tools.
- Infrastructure configuration must be reproducible via code (Docker, Helm, YAML).

## Constraints
- **Language (Backend)**: Python 3.13+
- **Frontend**: Next.js (App Router), TypeScript
- **Database**: Neon Serverless PostgreSQL
- **ORM**: SQLModel
- **Auth**: Better Auth with JWT
- **AI Framework**: OpenAI Agents SDK
- **Architecture**: Stateless FastAPI services
- **Deployment**:
  - Local: Docker, Minikube
  - Cloud: Kubernetes (DOKS / GKE / AKS)
- **No hardcoded secrets** in source code.
- **No direct database access** from AI agents outside MCP tools.

## Quality Rules
- Code must be readable, modular, and aligned with clean architecture principles.
- No unused endpoints, tools, or specs.
- All API routes must validate authentication.
- Errors must be handled explicitly with meaningful responses.
- Each service must be independently deployable.
- Specs must be updated when behavior changes.

## Success Criteria
- All phases implemented according to their specifications.
- Console app fully functional (Phase I).
- Secure multi-user web application with persistent storage (Phase II).
- AI chatbot correctly managing tasks via MCP tools (Phase III).
- Local Kubernetes deployment operational via Helm (Phase IV).
- Event-driven architecture functioning with Kafka and Dapr (Phase V).
- Repository demonstrates clear spec history and architectural evolution.
- System can recover state after restarts without data loss.

## Non-Goals
- No UI polish beyond functional clarity.
- No speculative features not defined in specs.
- No tightly coupled services or hidden shared state.
- No manual infrastructure changes outside declared configuration.

## Guiding Principle
> **Specifications govern behavior.
AI accelerates execution.
Architecture remains intentional.**
```

## Response Text
The project constitution has been successfully updated with the provided content. The template at `.specify/memory/constitution.md` has been fully populated with project-specific values, creating a comprehensive governance document that includes 6 core principles, key standards and constraints, quality rules, and success criteria. The constitution is now ready to guide the development of the todo system evolution project.

## Outcome
Created initial project constitution v1.0.0 with all specified principles and governance structure.