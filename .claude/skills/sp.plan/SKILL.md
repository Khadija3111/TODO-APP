# sp.plan Skill

## Description
Generate implementation plans based on specifications for the Evolution of Todo (Hackathon II) project.

## Purpose
This skill analyzes project specifications and generates detailed implementation plans that follow the project's architecture principles and technology stack requirements.

## Functionality
- Reads feature specifications from the /specs folder
- Generates step-by-step implementation plans following clean architecture
- Considers the technology stack: FastAPI, Next.js, SQLModel, PostgreSQL, OpenAI Agents SDK
- Creates plans that align with the project constitution and design principles
- Produces plans that are spec-driven and AI-native ready

## Tech Stack Awareness
- Backend: Python 3.13+, FastAPI, SQLModel, PostgreSQL
- Frontend: Next.js 14+, TypeScript, Tailwind CSS
- AI Integration: OpenAI Agents SDK, Model Context Protocol (MCP)
- Infrastructure: Kafka (Redpanda), Dapr, Docker, Kubernetes

## Output Format
- Detailed implementation steps
- Technology recommendations
- Integration points
- Testing considerations
- Deployment requirements

## Constraints
- Plans must align with existing project architecture
- Follow clean code and statelessness principles
- Maintain separation of concerns
- Consider security requirements (JWT authentication)
- Account for AI-native architecture patterns