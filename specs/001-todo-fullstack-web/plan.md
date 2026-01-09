# PHASE II PLAN — TODO FULL-STACK WEB APPLICATION
(Spec-Driven | Agentic Dev Stack)

## OBJECTIVE
Transform the Phase I console Todo app into a secure, multi-user full-stack web application using Spec-Kit Plus and Claude Code, with no manual coding, persistent storage, and JWT-based authentication.

## ARCHITECTURE OVERVIEW

### Frontend (Next.js App Router)
- Better Auth (JWT enabled)
- Central API client (`/lib/api.ts`)
- Server + Client Components
- Sends `Authorization: Bearer <JWT>`

### Backend (FastAPI)
- JWT verification middleware
- REST API under `/api`
- SQLModel ORM
- User-scoped queries only

### Database (Neon Serverless PostgreSQL)
- `tasks` table (indexed by `user_id`)
- Users managed by Better Auth

## SECTION STRUCTURE

### Overview
Phase II scope and constraints with multi-user and authentication focus. The application will be built following spec-driven development principles with agentic development using Claude Code.

### Architecture
Frontend ↔ Backend ↔ Database with JWT trust boundary. All communication will be secured through JWT authentication tokens.

### Features
- Task CRUD operations
- User authentication and authorization
- User data isolation
- Task completion toggling
- Priority and category assignment

### API
- REST endpoints following standard conventions
- JWT authentication requirements on all endpoints
- Consistent error behavior and responses
- Proper HTTP status codes

### Database
- SQLModel schema definitions
- Indexing strategy for optimal performance
- User-scoped data isolation
- Proper relationships and constraints

### UI
- Pages for authentication, task management, and user dashboard
- Reusable components for consistent UX
- Loading, error, and empty states
- Responsive design patterns

## RESEARCH APPROACH
Research while writing specs (no large upfront research). Focused micro-research only:
- Better Auth JWT plugin
- FastAPI JWT verification
- Neon + SQLModel patterns
- Update specs immediately if assumptions change
- External references documented using APA style

## DECISIONS DOCUMENTATION

### Authentication Strategy
- Session cookies ❌
- JWT via Better Auth ✅
- Tradeoff: Stateless, scalable, shared secret required

### User Identity Source
- URL user_id
- JWT user_id ✅ (source of truth)

### Repository Structure
- Separate repos ❌
- Monorepo ✅
- Reason: Single Claude Code context

### API Protection
- Route-level checks
- JWT middleware + dependency injection ✅

## QUALITY VALIDATION
- Each feature mapped to acceptance criteria
- Specs reviewed before implementation
- Claude Code output validated against:
  - Specifications
  - Security rules
  - Folder and CLAUDE.md conventions
- No undocumented logic allowed

## TESTING STRATEGY

### Validation Checks
- Requests without JWT return 401
- Users cannot access other users' tasks
- CRUD operations persist in database
- Task completion toggle works correctly
- Frontend reflects backend state

### Testing Levels
- API: FastAPI route tests
- Integration: Auth → API → DB
- UI: Manual acceptance testing using specs

## PHASE ORGANIZATION

### 1. Research
- JWT flow patterns
- Better Auth configuration
- SQLModel + Neon setup
- Next.js App Router best practices
- Frontend-first development patterns

### 2. Foundation
- Monorepo + Spec-Kit structure
- CLAUDE.md files for both frontend and backend
- Base FastAPI and Next.js setup
- Initial project scaffolding

### 3. Frontend-First Implementation
- Design and implement UI components with mock data
- Define API contracts based on UI requirements
- Validate user flows and experiences
- Create API client structure with mock responses

### 4. Backend Implementation
- Build backend services to match defined API contracts
- Implement JWT middleware and authentication
- Create database models based on UI needs
- Build secure API endpoints with user isolation

### 5. Integration & Synthesis
- Connect frontend to backend APIs
- Conduct security validation
- Perform user isolation testing
- Optimize performance and user experience
- Final validation against specifications

## IMPLEMENTATION ROADMAP

### Phase 1: Foundation Setup
1. Create monorepo structure (`/frontend`, `/backend`, `/specs`)
2. Set up Next.js 14+ with App Router and TypeScript
3. Set up FastAPI with SQLModel and PostgreSQL connection
4. Configure Better Auth with JWT
5. Set up Claude Code agents for frontend and backend

### Phase 2: Frontend-First Implementation
1. Create authentication components and pages (with mock data)
2. Build task management UI components (with mock data)
3. Design dashboard and task list views
4. Implement API client structure with mock responses
5. Add loading, error, and empty states
6. Define API contracts and data structures based on UI needs
7. Validate user flows and experiences with mock implementations

### Phase 3: Backend Implementation
1. Implement JWT middleware for authentication
2. Create SQLModel database models based on UI requirements
3. Build secure API endpoints with user isolation (matching defined contracts)
4. Implement CRUD operations for tasks
5. Add task completion and organization features
6. Ensure all endpoints match the API contracts defined in frontend

### Phase 4: Integration & Testing
1. Connect frontend to backend APIs
2. Conduct security validation
3. Perform user isolation testing
4. Optimize performance and user experience
5. Final validation against specifications

## OUTCOME
A secure, spec-driven Phase II Todo application where:
- Authentication is enforced everywhere
- Users only access their own data
- Claude Code operates across frontend and backend
- The system is ready for Phase III (Chatbot)
- All functionality meets the measurable success criteria defined in the spec
- Frontend-first approach ensures optimal user experience and clear API contracts