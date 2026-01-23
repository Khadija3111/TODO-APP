# Todo AI Chatbot with MCP Integration

A comprehensive full-stack todo application featuring modern web technologies with authentication, database persistence, responsive UI, and AI-powered natural language task management.

## Live Demo

- **Frontend URL (Vercel)**: [https://todo-app-2-git-001-todo-fullstack-web-khadija3111s-projects.vercel.app/](https://todo-app-2-git-001-todo-fullstack-web-khadija3111s-projects.vercel.app/)
- **Backend URL (Hugging Face)**: [https://khadija222-to-do-app-chatbot-phase.hf.space/](https://khadija222-to-do-app-chatbot-phase.hf.space/)

## Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.13+)
- **Database**: Neon Serverless PostgreSQL
- **ORM**: SQLModel for database modeling
- **Authentication**: JWT-based authentication with secure password hashing
- **API**: RESTful API endpoints with proper validation
- **AI Integration**: Cohere LLM with OpenAI Agents SDK
- **MCP Tools**: Model Context Protocol for standardized AI tool access

### Frontend
- **Framework**: Next.js 16+ (App Router)
- **Styling**: Tailwind CSS for responsive design
- **State Management**: React Context API for authentication state
- **Animations**: Framer Motion for smooth UI transitions
- **Type Safety**: TypeScript for enhanced development experience
- **AI Interface**: Custom chatbot integration for conversational AI interactions

### Development Tools
- **Package Manager**: uv (modern Python package manager)
- **Database Client**: psycopg2-binary for PostgreSQL connectivity
- **Authentication**: Better Auth for secure authentication flows
- **Testing**: Pytest for backend testing

## Features

- **Full-Stack Architecture**: Complete application with both backend and frontend
- **Authentication System**: Secure login and registration with JWT tokens
- **Database Integration**: Neon PostgreSQL database with SQLModel ORM
- **Task Management**: Create, read, update, and delete tasks
- **Responsive UI**: Mobile-friendly interface built with Next.js and Tailwind CSS
- **Real-time Updates**: Dynamic task management without page refresh
- **Priority Levels**: High, medium, and low priority task categorization
- **Search & Filter**: Advanced task filtering and search capabilities
- **Secure Storage**: Encrypted passwords and secure session management
- **AI-Powered Task Management**: Interact with your todo list using natural language
- **MCP Integration**: Uses standardized Model Context Protocol tools for secure task operations
- **Stateless Architecture**: Conversation history maintained in database for resilience
- **Multi-turn Conversations**: Context-aware interactions that span multiple messages
- **User Isolation**: Proper scoping of tasks and conversations per user

## Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.13+)
- **Database**: Neon Serverless PostgreSQL
- **ORM**: SQLModel for database modeling
- **Authentication**: JWT-based authentication with secure password hashing
- **API**: RESTful API endpoints with proper validation
- **AI Integration**: Cohere LLM with OpenAI Agents SDK
- **MCP Tools**: Model Context Protocol for standardized AI tool access

### Frontend
- **Framework**: Next.js 16+ (App Router)
- **Styling**: Tailwind CSS for responsive design
- **State Management**: React Context API for authentication state
- **Animations**: Framer Motion for smooth UI transitions
- **Type Safety**: TypeScript for enhanced development experience
- **AI Interface**: ChatKit for conversational AI interactions

### Development Tools
- **Package Manager**: uv (modern Python package manager)
- **Database Client**: psycopg2-binary for PostgreSQL connectivity
- **Authentication**: Better Auth for secure authentication flows
- **Testing**: Pytest for backend testing

## Architecture

### Backend Structure
```
backend/
├── api/                   # API endpoints
│   ├── auth.py           # Authentication routes
│   ├── tasks.py          # Task management routes
│   └── chat.py           # AI chatbot endpoint
├── models/               # Database models
│   ├── user.py           # User model
│   ├── task.py           # Task model
│   └── conversation.py   # Conversation and Message models
├── services/             # Business logic
│   ├── task_service.py   # Task operations
│   ├── conversation_service.py # Conversation operations
│   └── message_service.py # Message operations
├── mcp/                  # Model Context Protocol server
│   ├── server.py         # MCP server
│   └── tools/
│       └── task_operations.py # Task MCP tools
├── agents/               # AI agent configuration
│   ├── config.py         # Agent configuration
│   └── chat_agent.py     # Chat agent implementation
├── utils/                # Utility functions
│   ├── auth.py           # Authentication utilities
│   └── database.py       # Database utilities
└── main.py               # Application entry point
```

### Frontend Structure
```
frontend/
├── src/
│   └── app/              # Next.js App Router pages
│       ├── auth/         # Authentication pages
│       ├── dashboard/    # Dashboard page
│       ├── layout.tsx    # Root layout
│       └── page.tsx      # Home page
├── lib/
│   └── api.ts           # API client configuration
├── components/          # Reusable React components
│   ├── ChatbotIcon.jsx  # AI chatbot icon
│   └── ChatPanel.jsx    # AI chatbot panel
├── utils/
│   └── api.js           # API utilities for chatbot
└── context/             # React Context providers
```

## Setup & Installation

### Prerequisites
- Node.js 18+
- Python 3.13+
- uv package manager
- Access to Neon PostgreSQL database

### Installation Steps

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd TODO
   ```

2. Install Python dependencies:
   ```bash
   uv pip install -r requirements.txt
   # Or if using pyproject.toml:
   uv sync
   ```

3. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

4. Configure environment variables:
   ```bash
   # In the frontend directory
   NEXT_PUBLIC_API_URL=http://localhost:8001/api
   ```

5. Set up the database connection in backend configuration

6. Start the backend server:
   ```bash
   uv run uvicorn backend.main:app --reload --port 8001
   ```

7. Start the frontend development server:
   ```bash
   cd frontend
   npm run dev
   ```

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user profile

### Task Management
- `GET /api/tasks` - Get all tasks
- `POST /api/tasks` - Create a new task
- `PUT /api/tasks/{id}` - Update a task
- `DELETE /api/tasks/{id}` - Delete a task
- `PUT /api/tasks/{id}/complete` - Toggle task completion

### AI Chatbot
- `POST /api/{user_id}/chat` - Send message to AI chatbot
- `GET /api/{user_id}/conversations` - Get user's conversations
- `GET /api/{user_id}/conversations/{conversation_id}` - Get messages for a conversation

### MCP Tools
The AI chatbot uses Model Context Protocol (MCP) tools to perform task operations:
- `add_task` - Create a new task with title, description, priority, and category
- `list_tasks` - Retrieve all tasks for the authenticated user
- `complete_task` - Mark a specific task as complete/incomplete
- `delete_task` - Remove a task from the user's list
- `update_task` - Modify task properties including title, description, priority, and category

## Database Schema

### Users Table
- `id`: UUID primary key
- `email`: User's email address (unique)
- `hashed_password`: BCrypt hashed password
- `created_at`: Account creation timestamp
- `updated_at`: Last update timestamp

### Tasks Table
- `id`: UUID primary key
- `user_id`: Foreign key linking to user
- `title`: Task title
- `description`: Optional task description
- `completed`: Boolean indicating completion status
- `priority`: Enum (low, medium, high)
- `category`: Optional category
- `tags`: JSON string for task tags
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Conversations Table
- `id`: UUID primary key
- `user_id`: Foreign key linking to user
- `title`: Conversation title (auto-generated from first message)
- `created_at`: Conversation creation timestamp
- `updated_at`: Last update timestamp

### Messages Table
- `id`: UUID primary key
- `conversation_id`: Foreign key linking to conversation
- `role`: Message role (user or assistant)
- `content`: Message content
- `tool_calls`: JSON array of tool calls made during the message
- `tool_results`: JSON array of results from tool calls
- `created_at`: Message creation timestamp

## Environment Variables

### Backend
- `SECRET_KEY`: JWT secret key for token encryption
- `DATABASE_URL`: PostgreSQL database connection string
- `COHERE_API_KEY`: API key for Cohere integration
- `COHERE_MODEL`: Cohere model to use (default: command-r-plus)
- `AGENT_TEMPERATURE`: Temperature setting for AI agent (default: 0.7)
- `AGENT_MAX_TOKENS`: Maximum tokens for AI agent (default: 2000)

### Frontend
- `NEXT_PUBLIC_API_URL`: Backend API base URL

## Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: BCrypt with 12 rounds for secure password storage
- **Input Validation**: Comprehensive validation on both frontend and backend
- **SQL Injection Prevention**: ORM-based queries prevent SQL injection
- **XSS Protection**: Input sanitization and proper output encoding
- **MCP Tool Scoping**: All AI operations are properly scoped to user ID to prevent unauthorized access
- **AI Input Sanitization**: Natural language inputs are validated before processing
- **Conversation Isolation**: User conversations are isolated and protected by user ID scoping

## Deployment

### Backend Deployment
- Deploy to cloud platforms supporting Python applications
- Configure environment variables for production including Cohere API key
- Set up SSL certificates for secure connections
- Ensure MCP server is properly configured in production
- Configure proper rate limiting for AI API calls

### Frontend Deployment
- Deploy to Vercel, Netlify, or similar platforms
- Configure environment variables for production API endpoints
- Set up custom domain if needed
- Ensure CORS policies allow communication with backend

### AI Chatbot Considerations
- Secure storage of Cohere API key in production environment
- Monitor AI token usage and costs
- Implement proper error handling for AI service outages
- Set up logging for AI interactions for debugging and monitoring

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- FastAPI for the excellent web framework
- Next.js for the powerful React framework
- SQLModel for seamless database integration
- Neon for serverless PostgreSQL hosting
- Cohere for the powerful language model API
- OpenAI for the Agents SDK framework
- Model Context Protocol (MCP) for standardized AI tool integration
- The open-source community for amazing tools and libraries