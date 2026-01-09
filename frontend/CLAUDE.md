# Claude Code Instructions: Frontend

## Project Overview

This is the frontend of the Todo Full-Stack Web Application built with Next.js 14+, TypeScript, and Tailwind CSS. The application uses Better Auth for JWT-based authentication and communicates with the backend via API calls.

## Architecture

The frontend follows these patterns:
- Next.js App Router for routing
- Server and Client Components
- TypeScript for type safety
- Tailwind CSS for styling
- Better Auth for authentication
- Central API client for backend communication

## Code Standards

- Follow TypeScript best practices
- Use Tailwind CSS utility classes
- Implement responsive design patterns
- Follow accessibility guidelines (ARIA attributes)
- Use Next.js Image component for images
- Follow Next.js best practices for performance

## File Structure

```
frontend/
├── src/
│   └── app/                 # Next.js App Router pages
│       ├── auth/            # Authentication pages
│       ├── dashboard/       # Dashboard pages
│       ├── tasks/           # Task management pages
│       ├── layout.tsx       # Root layout
│       └── page.tsx         # Home page
├── lib/
│   └── api.ts              # API client
├── components/             # Reusable components
├── types/                  # TypeScript type definitions
└── CLAUDE.md               # This file
```

## Development Guidelines

- Use Server Components for data fetching when possible
- Use Client Components for interactivity
- Implement proper loading and error states
- Follow Next.js Image optimization practices
- Use environment variables for configuration
- Implement proper error boundaries
- Follow accessibility best practices