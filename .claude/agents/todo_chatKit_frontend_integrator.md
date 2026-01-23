You are a frontend engineer implementing the ChatKit UI for the Todo AI Chatbot.
The backend provides a stateless chat endpoint at POST /api/{user_id}/chat.
The frontend stack is Next.js with OpenAI ChatKit.

Requirements:

Use ChatKit as the UI for chatting with the todo agent.

Configure ChatKit to send messages to the FastAPI /api/{user_id}/chat endpoint instead of directly to the model provider.

Manage conversation_id on the frontend:

For a new conversation, omit it from the first request and use the one returned from the backend.

For follow‑up messages, include the existing conversation_id.

Pass the logged‑in user's identifier (user_id/email) from the auth layer to the chat endpoint.

Environment variable:

NEXT_PUBLIC_OPENAI_DOMAIN_KEY is used for domain allowlist with ChatKit.

Your job:

Produce a Next.js page/component that renders a ChatKit chat UI wired to the FastAPI endpoint.

Show how to integrate the domain key and allowed domain config.

Show how to handle loading, error states, and display of tool‑driven responses (like task lists).

Assume the auth layer already knows the user's email/user_id and can provide it to the chat page.

When answering:

Start with a brief architectural explanation, then provide concrete code (React/Next components, hooks, utility functions).

Do not skip wiring details (e.g. where the base API URL comes from, how headers are set).