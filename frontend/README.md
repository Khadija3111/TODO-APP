# Todo App Frontend

A modern, full-stack todo application with authentication and AI-powered chatbot integration.

## Features

- User authentication (register/login)
- Task management (create, read, update, delete)
- Task filtering and sorting
- Real-time chatbot integration
- Responsive design

## Tech Stack

- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- Framer Motion (animations)
- React Context (state management)

## Environment Variables

Create a `.env.local` file in the root of the frontend directory with the following variables:

```env
# API URL for the backend service
NEXT_PUBLIC_API_URL=https://your-backend-url.com

# Better Auth Secret (set in production environment)
BETTER_AUTH_SECRET=your-secret-key

# Cohere API Key (for chatbot functionality)
COHERE_API_KEY=your-cohere-api-key
```

For production deployment, make sure to set these environment variables in your hosting platform instead of committing them to version control.

## Installation

1. Install dependencies:
```bash
npm install
```

2. Run the development server:
```bash
npm run dev
```

3. Open [http://localhost:3000](http://localhost:3000) to view the application in your browser.

## Building for Production

To build the application for production:

```bash
npm run build
```

## Deployment

This application is optimized for deployment on platforms like Vercel, Netlify, or other hosting providers that support Next.js applications.

### Deploying to Vercel

1. Push your code to a Git repository
2. Import your project into Vercel
3. Set the environment variables in the Vercel dashboard
4. Deploy!

### Environment Configuration for Production

Make sure to set these environment variables in your production environment:

- `NEXT_PUBLIC_API_URL`: The URL of your deployed backend API
- `BETTER_AUTH_SECRET`: Your secret key for authentication
- `COHERE_API_KEY`: Your Cohere API key for chatbot functionality

## API Integration

The frontend communicates with the backend API through the centralized API client located at `lib/api.ts`. The application supports both local development and remote production API endpoints through environment variable configuration.

## Security Notes

- Never commit sensitive API keys to version control
- Use environment variables for all sensitive configuration
- The application uses JWT tokens stored in localStorage for authentication