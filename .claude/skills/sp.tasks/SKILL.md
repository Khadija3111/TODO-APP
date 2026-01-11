# sp.tasks Skill

## Description
Generate actionable, dependency-ordered task lists for the Evolution of Todo (Hackathon II) project based on specifications and implementation plans.

## Purpose
This skill creates structured, prioritized task lists that follow the project's architecture and development workflow requirements.

## Functionality
- Reads specifications and implementation plans from project artifacts
- Generates dependency-ordered task lists with clear action items
- Ensures tasks align with the technology stack and project constraints
- Creates tasks that follow spec-driven development principles
- Orders tasks by dependency relationships and development phases
- Includes testing and validation tasks

## Tech Stack Awareness
- Backend: Python 3.13+, FastAPI, SQLModel, PostgreSQL
- Frontend: Next.js 14+, TypeScript, Tailwind CSS
- AI Integration: OpenAI Agents SDK, Model Context Protocol (MCP)
- Infrastructure: Kafka (Redpanda), Dapr, Docker, Kubernetes

## Output Format
- Numbered, dependency-ordered task list
- Clear action items with specific deliverables
- Task dependencies and relationships
- Technology-specific implementation notes
- Testing and validation tasks

## Constraints
- Tasks must follow the project's evolutionary growth approach
- Maintain separation between frontend, backend, and AI components
- Respect the monorepo structure (/frontend, /backend, /specs)
- Include security considerations (JWT authentication)
- Account for distributed system requirements
- Ensure tasks are measurable and verifiable