<!--
Sync Impact Report:
- Version change: 1.1.0 → 1.2.0
- Modified principles: Updated to include new intermediate and advanced features
- Added sections: Priorities & Tags, Search & Filter, Sort, Recurring Tasks, Due Dates & Reminders
- Removed sections: None
- Templates requiring updates:
  - .specify/templates/plan-template.md ✅ updated
  - .specify/templates/spec-template.md ✅ updated
  - .specify/templates/tasks-template.md ✅ updated
  - .specify/templates/commands/*.md ⚠ pending
- Follow-up TODOs: None
-->
# Project Constitution: Evolution of Todo (Hackathon II)

## Project: Evolution of Todo: From CLI to AI-Native Distributed Systems

## Core Principles

• **Spec-Driven Development**: Implementation must always follow specifications managed by GitHub Spec-Kit Plus and Claude Code.

• **AI-Native Architecture**: Prioritize the use of AI agents (Claude Code, Gordon, kubectl-ai) to build complex systems without writing boilerplate code.

• **Clean Code & Statelessness**: Adherence to clean code principles and a strictly stateless backend architecture to ensure scalability and resilience.

• **Evolutionary Growth**: Software must progress systematically from a simple CLI to a cloud-native, event-driven distributed system.

## Key Standards

• **Technology Stack**:
    ◦ Backend: Python 3.13+, FastAPI, SQLModel (ORM), and Neon Serverless PostgreSQL.
    ◦ Frontend: Next.js 14+ (App Router), TypeScript, and Tailwind CSS.
    ◦ AI Integration: OpenAI Agents SDK and Model Context Protocol (MCP) for tool-based task management.
    ◦ Infrastructure: Kafka (via Redpanda) for event-driven features and Dapr for distributed runtime building blocks.

• **Security**: Mandatory JWT-based authentication using Better Auth; all API requests must be verified and filtered by user ID.

• **Project Structure**: A Monorepo organization containing /frontend, /backend, and a structured /specs folder is required for single-context AI development.

• **API Conventions**: All RESTful endpoints must reside under /api/ and return JSON responses using Pydantic models.

## Constraints

• **Development Workflow**: Developers must read the relevant spec (@specs/...) before implementation and update specs if requirements change.

• **Tooling**: Use uv for Python management and WSL 2 for Windows-based development.

• **Deployment Pipeline**: Initial deployment on Minikube (local Kubernetes) followed by production-grade deployment on DigitalOcean, GKE, or AKS.

• **Messaging**: Kafka must be used for decoupling services like notifications and recurring task engines.

## Success Criteria

• **Feature Completeness**: Successful implementation of all 5 basic features (Add, Delete, Update, View, Mark Complete) across all five phases.

• **Conversational Competence**: The AI Chatbot must accurately manage tasks through natural language via MCP tools while maintaining conversation history in the database.

• **Infrastructure Automation**: Successful containerization and deployment using Helm charts and AI-assisted DevOps tools (kubectl-ai, Kagent).

• **System Integrity**: All claims and features must be verified against the project specifications and documentation in the final GitHub repository.

## Legacy Features (Previously Implemented)

### Already Implemented (Basic CLI)
- Add / Delete / Update / View tasks
- Mark as complete

### INTERMEDIATE FEATURES (CLI Usability)
1. **Priorities & Tags**
   - Task fields: `priority` (high/med/low), `tags[]` (e.g., work, home)
   - UI: dropdown for priority, multi-select chips for tags
   - ✅ Users can set/change priority & tags; list can be filtered by them.

2. **Search & Filter**
   - Search bar (title/description, case-insensitive)
   - Filter panel: status, priority, tags, date range
   - ✅ Real-time results; combined filters work; "no match" message shown.

3. **Sort**
   - Options: due date, priority, alphabetical, creation date (asc/desc)
   - Persist choice in local storage
   - ✅ Selecting a sort instantly reorders the list.

### ADVANCED FEATURES (CLI Intelligence)
4. **Recurring Tasks**
   - Field `recurrence` (none, daily, weekly, monthly, custom)
   - On completion, auto-create next instance with updated due date
   - ✅ Users set recurrence; completing generates next task preserving other data.

5. **Due Dates & Reminders**
   - Fields `dueDate` (+ optional `dueTime`)
   - Date-time picker UI
   - Browser notifications: 10 min before & at due time, with snooze option
   - ✅ Notifications fire (with permission); overdue tasks highlighted.

## Governance
Specifications govern behavior. AI accelerates execution. Architecture remains intentional.

**Version**: 2.0.0 | **Ratified**: 2026-01-05 | **Last Amended**: 2026-01-05