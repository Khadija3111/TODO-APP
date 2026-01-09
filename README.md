# Full-Stack Todo Application

A comprehensive full-stack todo application featuring modern web technologies with authentication, database persistence, and responsive UI.

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

## Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.13+)
- **Database**: Neon Serverless PostgreSQL
- **ORM**: SQLModel for database modeling
- **Authentication**: JWT-based authentication with secure password hashing
- **API**: RESTful API endpoints with proper validation

### Frontend
- **Framework**: Next.js 16+ (App Router)
- **Styling**: Tailwind CSS for responsive design
- **State Management**: React Context API for authentication state
- **Animations**: Framer Motion for smooth UI transitions
- **Type Safety**: TypeScript for enhanced development experience

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
│   └── tasks.py          # Task management routes
├── models/               # Database models
│   ├── user.py           # User model
│   └── task.py           # Task model
├── services/             # Business logic
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

## Environment Variables

### Backend
- `SECRET_KEY`: JWT secret key for token encryption
- `DATABASE_URL`: PostgreSQL database connection string

### Frontend
- `NEXT_PUBLIC_API_URL`: Backend API base URL

## Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: BCrypt with 12 rounds for secure password storage
- **Input Validation**: Comprehensive validation on both frontend and backend
- **SQL Injection Prevention**: ORM-based queries prevent SQL injection
- **XSS Protection**: Input sanitization and proper output encoding

## Deployment

### Backend Deployment
- Deploy to cloud platforms supporting Python applications
- Configure environment variables for production
- Set up SSL certificates for secure connections

### Frontend Deployment
- Deploy to Vercel, Netlify, or similar platforms
- Configure environment variables for production API endpoints
- Set up custom domain if needed

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
- The open-source community for amazing tools and libraries